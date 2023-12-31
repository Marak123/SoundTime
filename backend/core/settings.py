"""
Django settings for CoreRoot project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

# Application definition
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',

    'media',
    'apis',
    'apis.base',
    'apis.user',
    'apis.auth',
    'apis.song',
]

AUTH_USER_MODEL = 'apis_user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL          = '/static/'
MEDIA_URL           = '/media/'

MEDIA_ROOT          = os.environ.get('MEDIA_ROOT', '/usr/src/app/mediafiles')
STATIC_ROOT         = os.environ.get('STATIC_ROOT', '/usr/src/app/staticfiles')

MEDIA_URL_AUDIO     = 'audio/'
MEDIA_URL_THUMBNAIL = 'thumbnail/'

""" path to the folder where audio files will be saved """
OUTPUT_AUDIO_PATH   = f"{MEDIA_ROOT}/{os.environ.get('NAME_AUDIO_OUTPUT', 'audio')}/"

if not os.path.exists(OUTPUT_AUDIO_PATH):
    os.makedirs(OUTPUT_AUDIO_PATH)

""" path to the folder where image files will be saved """
OUTPUT_IMAGE_PATH   = f"{MEDIA_ROOT}/{os.environ.get('NAME_IMAGE_OUTPUT', 'images')}/"

if not os.path.exists(OUTPUT_IMAGE_PATH):
    os.makedirs(OUTPUT_IMAGE_PATH)

""" path to the folder where temporary files will be saved """
OUTPUT_TEMP_PATH    = f"{MEDIA_ROOT}/{os.environ.get('NAME_TEMP_OUTPUT', 'temp')}/"

if not os.path.exists(OUTPUT_TEMP_PATH):
    os.makedirs(OUTPUT_TEMP_PATH)


THUMBNAIL_NAME_RESOLUTION = {
    '144': 'thumbnail_144p.webp',
    '240': 'thumbnail_240p.webp',
    '360': 'thumbnail_360p.webp',
    '480': 'thumbnail_480p.webp',
    '720': 'thumbnail_720p.webp',
    'ORIGINAL': 'thumbnail_original.webp'
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_THROTTLE_RATES': {
        # 'login_attempts': '10/hour',  # Możesz dostosować liczbę prób logowania w jednostce czasu
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    "UPDATE_LAST_LOGIN": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

APPEND_SLASH=False

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True