"""
Django settings for url_Shortner project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from corsheaders.middleware import *
from pathlib import Path
from decouple import config
#import django_heroku

# Build paths inside the project like thisF: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #intalled APP
    'account',
    'api',
    "corsheaders",
    


    # install package
    'rest_framework',
    'django_filters',
     'django_user_agents',
     'rest_framework_simplejwt',
     'djoser',
     'drf_yasg',
     'django_extensions',
     'django_celery_beat'
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'api.middleware.SqlPrintingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'django_user_agents.middleware.UserAgentMiddleware',
     #'account.middleware.GetCurrentUserMiddleware',
    
]

import os

ROOT_URLCONF = 'url_shortner.urls'
GEOIP_PATH =os.path.join(BASE_DIR, 'geoip')
print(BASE_DIR)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'url_shortner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':"rest_framework.pagination.LimitOffsetPagination"
    ,
    "PAGE_SIZE":100,
     
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10002/day',
        'user': '1000/day'
    },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication']

}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
   'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = "account.UserAccount"

DJOSER = {
    "LOGIN_FIELD":"email",
    "SEND_CONFIRMATION_EMAIL":False,
    "USER_CREATE_PASSWORD_RETYPE":True,
    "PASSWORD_RESET_RETYPE":True,
    "USERNAME_RESET_CONFIRM_URL":"email/reset/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL":"email/reset/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL":"password/reset/{uid}/{token}",
    "ACTIVATION_URL":"activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL":True,
    'EMAIL':{
        "activation":"api.email_helper.ActivationEmail"
    }
   
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "haryournifemijt@gmail.com"
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

from corsheaders.defaults import default_headers

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS =True
CSRF_TRUSTED_ORIGINS = [
    "https://shortenr.vercel.app","http://localhost:3000","http://127.0.0.1:3000"
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "*"
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]



CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'



DATABASE_ROUTERS = [
  "url_shortner.db_router.ReplicationRouter"
]

