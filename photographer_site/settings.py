import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def env_int(name, default=0):
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def should_require_db_ssl(database_url):
    if not database_url:
        return False
    scheme = database_url.split(":", 1)[0].lower()
    return scheme in {"postgres", "postgresql", "mysql", "mysql2"}


IS_RENDER = os.getenv("RENDER", "").lower() == "true"
REPO_DB_PATH = BASE_DIR / "db.sqlite3"
USE_COMMITTED_SQLITE = env_bool(
    "USE_COMMITTED_SQLITE",
    default=IS_RENDER and REPO_DB_PATH.exists(),
)
PROJECT_PUBLIC_HOSTS = [
    "rjz-studio-obrazu-55.pl",
    "www.rjz-studio-obrazu-55.pl",
]

DEBUG = env_bool("DEBUG", default=not IS_RENDER)

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-secret-key-change-me-before-production"
    else:
        raise ImproperlyConfigured("SECRET_KEY env var is required when DEBUG=False.")

default_allowed_hosts = ["127.0.0.1", "localhost", "[::1]"]
if IS_RENDER:
    default_allowed_hosts.append(".onrender.com")
default_allowed_hosts.extend(PROJECT_PUBLIC_HOSTS)
render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    default_allowed_hosts.append(render_hostname)

ALLOWED_HOSTS = list(dict.fromkeys(default_allowed_hosts + env_list("ALLOWED_HOSTS")))

default_csrf_trusted_origins = []
if render_hostname:
    default_csrf_trusted_origins.append(f"https://{render_hostname}")
default_csrf_trusted_origins.extend([f"https://{host}" for host in PROJECT_PUBLIC_HOSTS])

CSRF_TRUSTED_ORIGINS = list(
    dict.fromkeys(default_csrf_trusted_origins + env_list("CSRF_TRUSTED_ORIGINS"))
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "portfolio.middleware.RenderHealthcheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "photographer_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "photographer_site.wsgi.application"

database_url = os.getenv("DATABASE_URL")
if USE_COMMITTED_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": REPO_DB_PATH,
        }
    }
elif database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=should_require_db_ssl(database_url),
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "portfolio.email_backend.GmailOAuth2EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN", "")
GMAIL_TOKEN_URI = os.getenv("GMAIL_TOKEN_URI", "https://oauth2.googleapis.com/token")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "noreply@example.com")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", EMAIL_HOST_USER or DEFAULT_FROM_EMAIL)

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=True)
    SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
    SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", default=False)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
