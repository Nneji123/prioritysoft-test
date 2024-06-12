import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    send_default_pii=True,
)


INSTALLED_APPS = INSTALLED_APPS + [
    "accounts",
    "core",
    "inventory",
]

SECRET_KEY = os.environ.get("PROD_SECRET_KEY")

DEBUG = False

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "request_logging.middleware.LoggingMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# CORS_ALLOW_ALL_ORIGINS: True

DATABASES = {
    "default": dj_database_url.config(default=os.environ.get("POSTGRES_URI")),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("PROD_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("PROD_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("PROD_EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("PROD_EMAIL_PORT")

REDIS_URL = os.environ.get("PROD_REDIS_URL")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
}
