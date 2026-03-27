from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse

from .email_backend import GmailOAuth2EmailBackend
from .models import ContactMessage
from .models import PortfolioPhoto


class PortfolioTemplateTests(TestCase):
    def test_portfolio_page_handles_titles_with_apostrophes(self):
        photo = PortfolioPhoto.objects.create(
            title="Jan's sesja",
            image="portfolio/test.jpg",
        )

        response = self.client.get(reverse("portfolio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-lightbox-alt="Jan&#x27;s sesja"')
        self.assertNotContains(response, 'onclick="openLightbox')
        self.assertContains(response, photo.image.url)


class GmailOAuth2EmailBackendTests(TestCase):
    def test_build_oauth2_string(self):
        auth_string = GmailOAuth2EmailBackend._build_oauth2_string(
            "test@example.com",
            "token-123",
        )

        self.assertEqual(
            auth_string,
            "user=test@example.com\x01auth=Bearer token-123\x01\x01",
        )

    @patch("portfolio.email_backend.request.urlopen")
    def test_get_access_token_uses_refresh_token_flow(self, mock_urlopen):
        backend = GmailOAuth2EmailBackend(username="test@example.com")
        response = MagicMock()
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        response.read.return_value = b'{"access_token": "access-123"}'
        mock_urlopen.return_value = response

        with patch("portfolio.email_backend.settings.GMAIL_CLIENT_ID", "client-id"), patch(
            "portfolio.email_backend.settings.GMAIL_CLIENT_SECRET",
            "client-secret",
        ), patch("portfolio.email_backend.settings.GMAIL_REFRESH_TOKEN", "refresh-token"):
            access_token = backend._get_access_token()

        self.assertEqual(access_token, "access-123")
        mock_urlopen.assert_called_once()


class ContactViewTests(TestCase):
    def test_contact_form_shows_success_message_when_email_is_sent(self):
        response = self.client.post(
            reverse("kontakt"),
            {
                "name": "Jan Kowalski",
                "email": "jan@example.com",
                "phone": "",
                "subject": "Sesja",
                "message": "Prosze o kontakt.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wiadomosc zostala wyslana. Odpowiem wkrotce.")
        self.assertEqual(ContactMessage.objects.count(), 1)

    @patch("portfolio.views.send_contact_notification", return_value=False)
    def test_contact_form_shows_warning_when_email_fails(self, _mock_send):
        response = self.client.post(
            reverse("kontakt"),
            {
                "name": "Jan Kowalski",
                "email": "jan@example.com",
                "phone": "",
                "subject": "Sesja",
                "message": "Prosze o kontakt.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Nie udalo sie wyslac maila. Twoja wiadomosc zostala zapisana, sprobuj ponownie za chwile.",
        )
        self.assertEqual(ContactMessage.objects.count(), 1)
