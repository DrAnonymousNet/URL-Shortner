from . import base
from decouple import config


DATABASES = {
  'default': {
    'ENGINE': 'django_psdb_engine',
    'NAME': config('DB_NAME'),
    'HOST': config('DB_HOST'),
    'PORT': config('DB_PORT'),
    'USER': config('DB_USER'),
    'PASSWORD': config('DB_PASSWORD'),
    'OPTIONS': {'ssl': False}
  }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config("REDIS_URL"),
        'TIMEOUT': 30,
        'KEY_PREFIX': "dev"
    }
}

ALLOWED_HOSTS = ["134.122.124.219","*"]