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


DEBUG = config('DEBUG', False, cast=bool)
ALLOWED_HOSTS = ["shortenr.herokuapp.com","*", "134.122.124.219"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 
#STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

django_heroku.settings(locals(),logging=False)
