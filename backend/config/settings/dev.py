from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

WAGTAILAPI_BASE_URL = "http://localhost:8000"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = 'noreply@example.com'

# 開発環境ではすべてのオリジンを許可
CORS_ALLOW_ALL_ORIGINS = True

# または、より詳細な制御が必要な場合
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "http://localhost:8080",
#     "http://127.0.0.1:8080",
# ]

# Cache Settings for Rate Limiting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-cache',
    }
}

# Contact App Rate Limiting (開発環境では緩めの設定)
CONTACT_RATE_LIMIT_MINUTE = 10
CONTACT_RATE_LIMIT_HOUR = 100
CONTACT_RATE_LIMIT_MINUTE_TIMEOUT = 60
CONTACT_RATE_LIMIT_HOUR_TIMEOUT = 3600

# Trusted Proxies (開発環境では全て信頼)
TRUSTED_PROXIES = ['127.0.0.1', 'localhost']