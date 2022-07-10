from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

from api.models import Link
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortner.settings')
app = Celery('url_shortner')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=12, day_of_the_month=30), clean_stale.s())


@app.task
def clean_stale():
    stale = Link.objects.find_stale()
    stale.delete()
    