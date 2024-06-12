import dj_database_url

from .base import *

INSTALLED_APPS = INSTALLED_APPS + [
    "accounts",
    "core",
    "inventory",
    "django_nose",
    "debug_toolbar",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middlewares.DisableCSRFMiddleware",  
"request_logging.middleware.LoggingMiddleware",
       "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SECRET_KEY = os.environ.get("DEV_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(default="sqlite:///./data/db.sqlite3"),
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = os.environ.get("DEV_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("DEV_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("DEV_EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("DEV_EMAIL_PORT")
EMAIL_SSL_CERTFILE = os.path.join(BASE_DIR, "data/cert.pem")
EMAIL_SSL_KEYFILE = os.path.join(BASE_DIR, "data/key.pem")

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=core",
]

REDIS_URL = os.environ.get("DEV_REDIS_URL")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


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
