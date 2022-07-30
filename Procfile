web: gunicorn url_shortner.wsgi
worker: celery -A url_shortner beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

