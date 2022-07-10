from .base import *



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''

DATABASES = {
  'default': {
    'ENGINE': 'django_psdb_engine',
    'NAME': config('DB_NAME'),
    'HOST': config('DB_HOST'),
    'PORT': config('DB_PORT'),
    'USER': config('DB_USER'),
    'PASSWORD': config('DB_PASSWORD'),
    'OPTIONS': {'ssl': {'ca': config('MYSQL_ATTR_SSL_CA')}}
  }
}
'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 30,
        'KEY_PREFIX': "dev"
    }
}

BROKER_URL =  'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND =  'redis://127.0.0.1:6379/1'

HOST = "http://localhost:3000"
ALLOWED_HOSTS = []