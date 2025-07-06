from .base import *
from .logging import LOGGING as LOGGING_CONFIG
import os


DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

WAGTAILAPI_BASE_URL = os.getenv("WAGTAILAPI_BASE_URL", "http://localhost")

WAGTAILADMIN_BASE_URL = os.getenv("WAGTAILADMIN_BASE_URL", "http://localhost")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# 本番環境用の設定（base.pyの設定を上書き）
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# プロキシ設定
USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # HTTPで動作中は無効化

# ミドルウェアにロギングを追加
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'home.middleware.RequestLoggingMiddleware',  # カスタムロギングミドルウェア
]

# CORS Settings for Production
# クレデンシャルを含むリクエストの許可
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else []

# HTTPS Security Settings
if os.getenv('USE_HTTPS', 'False') == 'True':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600  # 問題なければ1年（31536000）に変更
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Email Settings (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Contact App Rate Limiting
CONTACT_RATE_LIMIT_MINUTE = int(os.environ.get('CONTACT_RATE_LIMIT_MINUTE', '3'))
CONTACT_RATE_LIMIT_HOUR = int(os.environ.get('CONTACT_RATE_LIMIT_HOUR', '10'))
CONTACT_RATE_LIMIT_MINUTE_TIMEOUT = 60
CONTACT_RATE_LIMIT_HOUR_TIMEOUT = 3600

# Trusted Proxies (nginx in Docker network)
TRUSTED_PROXIES = os.getenv("TRUSTED_PROXIES", "").split(",") if os.getenv("TRUSTED_PROXIES") else ['nginx', '172.16.0.0/12', '192.168.0.0/16']

# Additional Security Headers for Production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Permissions Policy (Feature Policy)
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "geolocation": [],
    "microphone": [],
    "payment": [],
    "usb": []
}

LOGGING = LOGGING_CONFIG
