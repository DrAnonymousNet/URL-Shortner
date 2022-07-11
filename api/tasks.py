
from celery.schedules import crontab
from .models import Link
from url_shortner.celery import app


@app.shared
def clean_stale():
    stale = Link.objects.find_stale()
    stale.delete()
    