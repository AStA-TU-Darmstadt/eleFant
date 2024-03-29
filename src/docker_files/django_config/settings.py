"""
This is the default settings template for new EleFAnt installations.
Custom parameters are passed via the docker-compose command as environment variables
"""

import os, re
from django.utils.crypto import get_random_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Collect static files in a single directory
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEBUG=True


def generate_secret_key(path):
    """Generate a new secret_key file for new installations"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    with open(path, 'w') as f:
        s = "SECRET_KEY = '" + get_random_string(50, chars) + "'"
        f.write(s)


# use a different secret key in every installation
try:
    from .secret_key import SECRET_KEY
except ImportError:
    settings_dir = os.path.abspath(os.path.dirname(__file__))
    generate_secret_key(os.path.join(settings_dir, 'secret_key.py'))
    from .secret_key import SECRET_KEY

DEBUG = 'True' == os.environ.get('DEBUG')
# allowed hosts list can be seperated by comma, whitespace or both
ALLOWED_HOSTS = re.split(', | |,', os.environ.get('ALLOWED_HOSTS', '*'))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elefant',
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'django_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'de-de')

TIME_ZONE = os.environ.get('TIMEZONE', 'Europe/Berlin')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# E-mail Settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = 'True' == os.environ.get('EMAIL_USE_TLS', 'False')
if not EMAIL_USE_TLS:
    EMAIL_USE_SSL = 'True' == os.environ.get('EMAIL_USE_SSL', 'True')
EMAIL_SSL_CERTFILE = os.environ.get('EMAIL_SSL_CERTFILE')
EMAIL_SSL_KEYFILE = os.environ.get('EMAIL_SSL_KEYFILE')
