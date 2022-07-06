from calendar import calendar
from ipaddress import ip_address
from itertools import count
from os import device_encoding
import django

from django.db import models
from django.forms import Widget
from django.utils .translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models import F, Sum ,Q
from datetime import datetime, timedelta, date

from pytz import country_names
from .hash_generator import random_md5
import dateutil.tz
from django.http import HttpRequest, request
from django.core.validators import URLValidator


def get_start_and_end_date():
    today_date = date.today()
    start_week = today_date - timedelta(today_date.isoweekday())
    end_week = start_week + timedelta(7)
    return start_week, end_week


MONTH = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


User = get_user_model()
 

class LinkManager(models.Manager):

    def find_stale(self):
        tzinfo=dateutil.tz.tzoffset(None, 3*60*60)
        return self.annotate(days_of_inactive =datetime.now(tz=tzinfo).date() -  F("last_visited_date") ).filter(days_of_inactive__gte = timedelta(days = 1))



class AnalyticDateTimeManager(models.Manager):


    def get_by_current_month(self):
        return self.values("date").filter(date__month = datetime.now().date().month).annotate(Sum("count"))
    def get_today_total(self):
        return self.values("date").filter(date = datetime.now().date()).annotate(Sum("count"))
    def get_today_by_hour(self):
        return self.values("time__hour").filter(date = datetime.now().date()).annotate(Sum("count"))
    def get_this_week_by_day(self):
        startdate, enddate = get_start_and_end_date()
        return self.values("date").filter(Q(date__gte = startdate), Q(date__lt=enddate)).annotate(Sum("count"))

    



class Link(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_constraint=False)
    short_link = models.URLField(_("Short link"), editable=False)
    long_link = models.TextField(_("Long link"), blank=False, null=False, validators=[URLValidator])
    last_visited_date = models.DateField(_("last visited"), auto_now=True, editable=False)
    visit_count = models.PositiveBigIntegerField(_("visit count"),editable=False, default=0)
    date_created = models.DateField(auto_now_add=True)
    objects = LinkManager()
    



    def save(self, **kwargs) -> None:
        if not self.short_link:
            self.short_link = f"{request.get_host()}/{random_md5(self.long_link)[0]}"
        return super().save(**kwargs)



    def __str__(self) -> str:
        return self.short_link

    
class Analytic(models.Model):
    link = models.OneToOneField(Link, on_delete=models.CASCADE, db_constraint=False)
    #User Agent
    device = models.JSONField(default = dict)
    os = models.JSONField(default=dict)
    browser = models.JSONField(default=dict)
    referer = models.JSONField(default=dict)
    # Localization
    country = models.JSONField(default=dict)
    
    #objects = AnalyticManager()

    def __str__(self) -> str:
        return f"Analytic for {self.link}"



    


class AnalyticByDateTime(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    count = models.PositiveIntegerField(default=0)

    objects = AnalyticDateTimeManager()

    def __str__(self) -> str:
        return f"AnalyticByHour for {self.link}"

