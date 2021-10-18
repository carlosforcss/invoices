from .base import *
import os
import sentry_sdk
import environ
from sentry_sdk.integrations.django import DjangoIntegration

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
base_env = environ.Env(
    EMAIL_USE_TLS=(bool, True),
)

env = environ.Env(
    DB_HOST=(str, "db"),
    DB_PORT=(int, 5432),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.environ.get("SECRET_KEY")

LANGUAGE_CODE = env("LANGUAGE_CODE")
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_DATABASE"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

sentry_sdk.init(
    dsn=env("SENTRY_DNS"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
