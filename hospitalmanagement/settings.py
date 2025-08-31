import os
from decouple import config, Csv
import os
from dotenv import load_dotenv
import dj_database_url
load_dotenv()

# print("📌 Loaded ALLOWED_HOSTS:", config('ALLOWED_HOSTS'))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
ALLOWED_HOSTS = ["healthpay.up.railway.app", "localhost", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    "https://healthpay.up.railway.app",
]


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
    'chat',

    # Third-party apps
    'widget_tweaks',
    'storages',  # Required for Supabase storage backend
]

# ──────────────────────────────────────────────────────────────
# ⚙️ MIDDLEWARE
# ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files in production
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
# this is a simple SQLite database configuration
# but for development and testing, SQLite is sufficient

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# for production, you should use a more robust database like PostgreSQL or MySQL
# uncomment for production use with PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}



# DATABASES = {
#     'default': dj_database_url.config(default=os.environ.get("DATABASE_URL"))
# }

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable compressed and cached static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


#MEDIA_URL = "/media/"
#MEDIA_ROOT = BASE_DIR / "media"

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
# for local development, you can use the in-memory channel layer
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(config("REDIS_HOST"), config("REDIS_PORT", cast=int))],
#         },
#     },
# }

# for production, you should use Redis as the channel layer backend and uncomment below
REDIS_URL = os.environ.get(
    "REDIS_URL",
    # "redis://127.0.0.1:6379"  # fallback for local dev
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}








DEFAULT_FILE_STORAGE = "core.storage_backends.SupabaseStorage"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

# this is to ensure that the SupabaseStorage is used as the default storage backend 
# it is necessary to set it up in the settings
from core.storage_backends import SupabaseStorage
from django.core.files.storage import default_storage
default_storage._wrapped = SupabaseStorage() #it overrides the default storage backend with SupabaseStorage

