import json
from urllib import parse, request

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.smtp import DNS_NAME
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class GmailOAuth2EmailBackend(SMTPEmailBackend):
    """SMTP backend that supports Gmail OAuth2 refresh tokens."""

    def _oauth_enabled(self):
        return any(
            [
                settings.GMAIL_CLIENT_ID,
                settings.GMAIL_CLIENT_SECRET,
                settings.GMAIL_REFRESH_TOKEN,
            ]
        )

    def _missing_oauth_settings(self):
        required = {
            "EMAIL_HOST_USER": self.username,
            "GMAIL_CLIENT_ID": settings.GMAIL_CLIENT_ID,
            "GMAIL_CLIENT_SECRET": settings.GMAIL_CLIENT_SECRET,
            "GMAIL_REFRESH_TOKEN": settings.GMAIL_REFRESH_TOKEN,
        }
        return [name for name, value in required.items() if not value]

    def _get_access_token(self):
        missing = self._missing_oauth_settings()
        if missing:
            raise ImproperlyConfigured(
                "Missing Gmail OAuth settings: " + ", ".join(missing)
            )

        payload = parse.urlencode(
            {
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "refresh_token": settings.GMAIL_REFRESH_TOKEN,
                "grant_type": "refresh_token",
            }
        ).encode("ascii")

        token_request = request.Request(
            settings.GMAIL_TOKEN_URI,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        timeout = self.timeout if self.timeout is not None else 10
        with request.urlopen(token_request, timeout=timeout) as response:
            token_data = json.load(response)

        access_token = token_data.get("access_token")
        if not access_token:
            raise ImproperlyConfigured(
                "Google token response did not include access_token."
            )
        return access_token

    @staticmethod
    def _build_oauth2_string(username, access_token):
        return f"user={username}\x01auth=Bearer {access_token}\x01\x01"

    def open(self):
        if self.connection:
            return False

        connection_params = {"local_hostname": DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params["timeout"] = self.timeout
        if self.use_ssl:
            connection_params["context"] = self.ssl_context

        try:
            self.connection = self.connection_class(
                self.host,
                self.port,
                **connection_params,
            )
            self.connection.ehlo()

            if not self.use_ssl and self.use_tls:
                self.connection.starttls(context=self.ssl_context)
                self.connection.ehlo()

            if self._oauth_enabled():
                access_token = self._get_access_token()
                self.connection.auth(
                    "XOAUTH2",
                    lambda challenge=None: self._build_oauth2_string(
                        self.username,
                        access_token,
                    ),
                    initial_response_ok=True,
                )
            elif self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except OSError:
            if not self.fail_silently:
                raise
