"""
Django settings for avagen project.
"""

import os
import dj_database_url
from pathlib import Path
import json
from google.oauth2 import service_account
import cloudinary
import base64

BASE_DIR = Path(__file__).resolve().parent.parent

# Import environment variables
if os.path.exists(os.path.join(BASE_DIR, "env.py")):
    import env
# Cloudinary configuration (for media/images only)


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)

# Google Cloud Storage (Heroku-safe)


GS_BUCKET_NAME = "avagen-downloads"

if "GCS_KEY_BASE64" in os.environ:
    key_json = base64.b64decode(os.environ["GCS_KEY_BASE64"]).decode("utf-8")
    creds_dict = json.loads(key_json)
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        creds_dict
    )
elif "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
    creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        creds_dict
    )
else:
    GS_CREDENTIALS = None
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".herokuapp.com",
]

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
    # Other
    "crispy_forms",
    "home",
    "products",
    "cart",
    "checkout",
    "faq",
    "profiles",
    "reviews",
    "catalogue",
    "storages",
    "newsletter",
    "useraccount",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "avagen.middleware.Custom404RedirectMiddleware",
]

ROOT_URLCONF = "avagen.urls"

CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                # required by allauth
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

SITE_ID = 1

SITE_DOMAIN = "avagen.co.uk"

EMAIL_BACKEND = "avagen.email_backend.CustomEmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "avagen.studio@gmail.com"
EMAIL_HOST_PASSWORD = "wjnq hcnr itwb sspf"
DEFAULT_FROM_EMAIL = "avagen.studio@gmail.com"
EMAIL_SUBJECT_PREFIX = "[avagen.co.uk] "

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

# Additional allauth settings for password reset

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/accounts/login/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/profile/"

# Password reset settings

ACCOUNT_PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
ACCOUNT_PASSWORD_RESET_TOKEN_GENERATOR = (
    "allauth.account.utils.default_token_generator"
)

# Additional settings for better password reset experience

ACCOUNT_LOGIN_BY_EMAIL_ENABLED = True
ACCOUNT_LOGIN_BY_USERNAME_ENABLED = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/profile/"

# Email settings for better delivery

EMAIL_TIMEOUT = 30
EMAIL_USE_LOCALTIME = True

WSGI_APPLICATION = "avagen.wsgi.application"

DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator"
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# === FILE STORAGE CONFIG ===


if not DEBUG:
    # Use Cloudinary for regular media/images

    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

    # Use GCS for digital downloads if available, otherwise local filesystem

    if GS_CREDENTIALS is not None:
        DIGITAL_DOWNLOAD_STORAGE = (
            "avagen.storage_backends.GoogleCloudZipStorage"
        )
    else:
        DIGITAL_DOWNLOAD_STORAGE = (
            "django.core.files.storage.FileSystemStorage"
        )
else:
    # Development: local file storage for everything

    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    DIGITAL_DOWNLOAD_STORAGE = "django.core.files.storage.FileSystemStorage"
# === STRIPE ===


STRIPE_CURRENCY = "usd"
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WH_SECRET = os.getenv("STRIPE_WH_SECRET", "")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

X_FRAME_OPTIONS = "ALLOWALL"
