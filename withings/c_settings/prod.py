from withings.settings import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['*']

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DATABASES['log_db'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'log_db.sqlite3',
}

# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': '',
#     'USER': '',
#     'PASSWORD': '',
#     'HOST': 'localhost',
#     'PORT': '',
# }
#
# DATABASES['log_db'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': '',
#     'USER': '',
#     'PASSWORD': '',
#     'HOST': 'localhost',
#     'PORT': '',
# }
