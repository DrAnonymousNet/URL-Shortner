
from celery.schedules import crontab
from celery import shared_task
from .models import Link
from url_shortner.celery import app


@shared_task
def clean_stale():
    stale = Link.objects.find_stale()
    stale.delete()

@app.task
def print_hello():
    print("Hello World")

#celery -A url_shortner beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    