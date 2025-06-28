from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

WAGTAILAPI_BASE_URL = "http://localhost:8000"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"