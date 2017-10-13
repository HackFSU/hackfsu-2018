"""
Django settings for hackfsu_com project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from . import keys
import os
import re

URL_BASE = "https://hackfsu.com"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, './media'))
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

SECRET_KEY = keys.APP_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = keys.APP_DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'hackfsu.com',
    '.hackfsu.com',
	'192.168.99.100'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'api',
    'webapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.JsonLoader',
    'hackfsu_com.middleware.RestrictStaffToAdminMiddleware'
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


ROOT_URLCONF = 'hackfsu_com.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'webapp/build/views')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',           # allauth
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': keys.DB_NAME,
        'USER': keys.DB_USER,
        'PASSWORD': keys.DB_PASSWORD,
        'HOST': keys.DB_HOST,
        'PORT': keys.DB_PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'


USE_TZ = True               # Data is stored based on user timezone
TIME_ZONE = 'US/Eastern'    # Forms will expect this in templates (in admin) by default
USE_I18N = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, './static_collected')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'webapp/build/static'),
]

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi|pug|scss)$'),
    re.compile(r'^/node_modules/'),
    re.compile(r'/\.git.*')
]

# Add more strict rules in production TODO
# if not DEBUG:
#     MIDDLEWARE.extend([
#         'django.middleware.csrf.CsrfViewMiddleware'
#     ])
#
#     CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
#     CSRF_COOKIE_NAME = 'csrftoken'
#     CSRF_COOKIE_SECURE = 'TRUE'
#     CSRF_TRUSTED_ORIGINS = []

