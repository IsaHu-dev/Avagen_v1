"""
Django settings for avagen project.
"""

import os
import json
import base64
from pathlib import Path

import dj_database_url
from google.oauth2 import service_account
import cloudinary
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

# Load env.py locally if present
if os.path.exists(os.path.join(BASE_DIR, "env.py")):
    import env  # noqa: F401

# --------------------------------------------------------------------
# CORE / SECURITY
# --------------------------------------------------------------------

DEBUG = os.getenv("DEBUG", "True").lower() in ("1", "true", "yes")

SECRET_KEY = os.getenv("SECRET_KEY") or (
    get_random_secret_key() if DEBUG else None
)
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is required in production")

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
        "https://localhost",
        "https://127.0.0.1",
    ]
else:
    ALLOWED_HOSTS = os.getenv(
        "ALLOWED_HOSTS", "127.0.0.1,localhost,.herokuapp.com"
    ).split(",")
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]
    CSRF_TRUSTED_ORIGINS = [
        f"https://{h.lstrip('.')}" for h in ALLOWED_HOSTS if h
    ]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

X_FRAME_OPTIONS = "ALLOWALL"

# --------------------------------------------------------------------
# CLOUDINARY
# --------------------------------------------------------------------

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

# --------------------------------------------------------------------
# GOOGLE CLOUD STORAGE (Heroku-safe)
# --------------------------------------------------------------------

GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME", "avagen-downloads")
GS_CREDENTIALS = None

if os.getenv("GCS_KEY_BASE64"):
    key_json = base64.b64decode(os.environ["GCS_KEY_BASE64"]).decode("utf-8")
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(key_json)
    )
elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    )

# --------------------------------------------------------------------
# APPS
# --------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_countries",
    "cloudinary",
    "cloudinary_storage",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "storages",
    "home",
    "products",
    "cart",
    "checkout",
    "faq",
    "profiles.apps.ProfilesConfig",
    "reviews",
    "catalogue",
    "newsletter",
    "useraccount",
]

# --------------------------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "avagen.middleware.Custom404RedirectMiddleware",
]

ROOT_URLCONF = "avagen.urls"
WSGI_APPLICATION = "avagen.wsgi.application"

# --------------------------------------------------------------------
# CRISPY FORMS
# --------------------------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# --------------------------------------------------------------------
# TEMPLATES
# --------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates" / "allauth",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "products.context_processors.categories_context",
                "cart.context_processors.cart_context",
            ],
            "builtins": [
                "crispy_forms.templatetags.crispy_forms_tags",
                "crispy_forms.templatetags.crispy_forms_field",
            ],
        },
    },
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = int(os.getenv("SITE_ID", "1"))
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "avagen.co.uk")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if not DEBUG else "http"

# --------------------------------------------------------------------
# EMAIL (Works on Heroku + Local Development)
# --------------------------------------------------------------------

if DEBUG:
    # Local development: print emails to console
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "webmaster@localhost"

else:
    # Production (Heroku): send via Gmail SMTP
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        raise RuntimeError(
            "⚠️ EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set in Heroku "
            "config vars for password reset emails to work."
        )

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_TIMEOUT = 30
    EMAIL_USE_LOCALTIME = True
    EMAIL_SUBJECT_PREFIX = "[Avagen] "

EMAIL_BACKEND_FALLBACK = "django.core.mail.backends.console.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

# --------------------------------------------------------------------
# ALLAUTH
# --------------------------------------------------------------------

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = "/profile/"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = (
    "/accounts/login/"
)
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = (
    "/profile/"
)

ACCOUNT_PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
ACCOUNT_PASSWORD_RESET_TOKEN_GENERATOR = (
    "allauth.account.utils.default_token_generator"
)
ACCOUNT_PASSWORD_RESET_USE_SITES_DOMAIN = True
ACCOUNT_PASSWORD_RESET_REDIRECT_URL = "/accounts/login/"

ACCOUNT_PASSWORD_RESET_SEND_EMAIL = True
ACCOUNT_PASSWORD_RESET_CONFIRM = True
ACCOUNT_PASSWORD_RESET_CONFIRM_RETYPE = True

ACCOUNT_LOGIN_BY_EMAIL_ENABLED = True
ACCOUNT_LOGIN_BY_USERNAME_ENABLED = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/profile/"

# --------------------------------------------------------------------
# DATABASE
# --------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# --------------------------------------------------------------------
# PASSWORDS
# --------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        )
    },
]

# --------------------------------------------------------------------
# I18N / TZ
# --------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------------------
# FILE STORAGE
# --------------------------------------------------------------------

if not DEBUG:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    if GS_CREDENTIALS:
        DIGITAL_DOWNLOAD_STORAGE = (
            "avagen.storage_backends.GoogleCloudZipStorage"
        )
    else:
        DIGITAL_DOWNLOAD_STORAGE = (
            "django.core.files.storage.FileSystemStorage"
        )
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    DIGITAL_DOWNLOAD_STORAGE = "django.core.files.storage.FileSystemStorage"

# --------------------------------------------------------------------
# STRIPE
# --------------------------------------------------------------------

STRIPE_CURRENCY = os.getenv("STRIPE_CURRENCY", "usd")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WH_SECRET = os.getenv("STRIPE_WH_SECRET", "")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
