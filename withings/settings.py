import datetime
from pathlib import Path
import os
import environ
from datetime import timedelta
from rest_framework.settings import api_settings

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django_crontab',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'corsheaders',
    'django_jalali',
    'rest_framework',
    'knox',
    'custom_logs',
    'account',
    'healthcare',
    'website',
    'docs',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'withings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'withings.wsgi.application'

DATABASES = {}

DATABASE_ROUTERS = ["withings.db_router.DbRouter", ]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 40
}

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(hours=240),
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': 10,
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': '%Y/%m/%d %H:%M',
    'AUTH_HEADER_PREFIX': 'BatoboxToken',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

CORS_ALLOW_ALL_ORIGINS = True

BASE_URL = 'https://withings.a-fathollahi.com/'

BASE_FRONT_URL = 'https://withings.a-fathollahi.com/'

BASE_CONTENT_URL = 'https://withings.a-fathollahi.com/'

OAUTH2_CALLBACK_URL = 'https://withings.a-fathollahi.com/account/auth2_callback/'

WHITINGS_API_Endpoint = 'https://wbsapi.withings.net'

CLIENT_ID = env('CLIENT_ID')
SECRET = env('SECRET')


FITBIT_OAUTH2_CALLBACK_URL = 'https://withings.a-fathollahi.com/account/fitbit-auth2-callback/'
FITBIT_API_Endpoint = 'https://wbsapi.withings.net'

FITBIT_CLIENT_ID = env('FITBIT_CLIENT_ID')
FITBIT_SECRET = env('FITBIT_SECRET')