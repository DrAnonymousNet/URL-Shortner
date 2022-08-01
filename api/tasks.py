
from celery.schedules import crontab
from celery import shared_task
from .models import Link
from url_shortner.celery import app


@app.task
def clean_stale():
    stale = Link.objects.find_stale()
    stale.delete()
    other_stale = Link.objects.find_unvisited()
    other_stale.dalete()


# celery -A url_shortner beat -l info --scheduler
# django_celery_beat.schedulers:DatabaseScheduler
