from .base import *
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.environ.get("SECRET_KEY")

CLOUDINARY = {
    "cloud_name": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "api_key": os.environ.get("CLOUDINARY_API_KEY"),
    "api_secret": os.environ.get("CLOUDINARY_API_SECRET"),
}

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST", "db"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DNS"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
