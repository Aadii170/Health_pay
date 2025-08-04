import os
from decouple import config, Csv

# ──────────────────────────────────────────────────────────────
# 📁 BASE DIRECTORY
# ──────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# ──────────────────────────────────────────────────────────────
# 🔐 SECURITY SETTINGS
# ──────────────────────────────────────────────────────────────

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv)

# ──────────────────────────────────────────────────────────────
# 🧩 INSTALLED APPS
# ──────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'channels',  # WebSocket support

    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'hospital',
    'doctor',
    'patient',
    'pathologist',

    # Third-party apps
    'widget_tweaks',
]

# ──────────────────────────────────────────────────────────────
# ⚙️ MIDDLEWARE
# ──────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ──────────────────────────────────────────────────────────────
# 🌐 URL & ASGI SETTINGS
# ──────────────────────────────────────────────────────────────

ROOT_URLCONF = 'hospitalmanagement.urls'
ASGI_APPLICATION = 'hospitalmanagement.asgi.application'

# ──────────────────────────────────────────────────────────────
# 📁 TEMPLATE CONFIGURATION
# ──────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ──────────────────────────────────────────────────────────────
# 🗄️ DATABASE CONFIGURATION
# ──────────────────────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# ──────────────────────────────────────────────────────────────
# 🔐 PASSWORD VALIDATION
# ──────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────
# 🌍 INTERNATIONALIZATION
# ──────────────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────
# 🖼️ STATIC & MEDIA FILES
# ──────────────────────────────────────────────────────────────

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ──────────────────────────────────────────────────────────────
# 🔐 AUTHENTICATION
# ──────────────────────────────────────────────────────────────

LOGIN_REDIRECT_URL = '/afterlogin'

# ──────────────────────────────────────────────────────────────
# 📧 EMAIL CONFIGURATION
# ──────────────────────────────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_RECEIVING_USER = [config('EMAIL_RECEIVING_USER')]
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ──────────────────────────────────────────────────────────────
# 🔌 CHANNELS CONFIGURATION (WebSockets)
# ──────────────────────────────────────────────────────────────

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config("REDIS_HOST"), config("REDIS_PORT", cast=int))],
        },
    },
}
