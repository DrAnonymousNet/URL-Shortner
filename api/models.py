from calendar import calendar
from ipaddress import ip_address
from itertools import count
from os import device_encoding

from django.db import models
from django.utils .translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from datetime import datetime, timedelta

from pytz import country_names
from .hash_generator import random_md5
import dateutil.tz
from django.http import HttpRequest, request
from .analytic import *






User = get_user_model()
 

class LinkManager(models.Manager):

    def find_stale(self):
        tzinfo=dateutil.tz.tzoffset(None, 3*60*60)
        return self.annotate(days_of_inactive =datetime.now(tz=tzinfo).date() -  F("last_visited_date") ).filter(days_of_inactive__gte = timedelta(days = 1))

     


class AnalyticDateTimeManager(models.Manager):
    def get_per_day_per_link(self):
        self.values("date", "link").annotate(Sum("count"))

    def get_last_30_days_per_link(self):
        self.values("date", "link").filter(date__gte = F("date") - timedelta(days=30)).annotate(Sum("count"))

    def get_last_7_days_per_link(self):
        AnalyticByDateTime.objects.values("date", "link").filter(date__gte = F("date") - timedelta(days=7)).annotate(Sum("count"))

    
    datetime.now().date().isocalendar()


class Link(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    short_link = models.URLField(_("Short link"), editable=False)
    long_link = models.URLField(_("Long link"), blank=False, null=False)
    last_visited_date = models.DateField(_("last visited"), auto_now=True, editable=False)
    visit_count = models.PositiveBigIntegerField(_("visit count"),editable=False, default=0)
    
    objects = LinkManager()

    class Meta:
        unique_together = ["owner", "long_link", "short_link"]


    def save(self, **kwargs) -> None:
        if not self.short_link:
            self.short_link = f"{request.get_host()}/{random_md5(self.long_link)[0]}"
        return super().save(**kwargs)



    def __str__(self) -> str:
        return self.short_link

    
class Analytic(models.Model):
    link = models.OneToOneField(Link, on_delete=models.CASCADE)
    #User Agent
    device = models.JSONField(default = dict)
    os = models.JSONField(default=dict)
    browser = models.JSONField(default=dict)
    refer = models.JSONField(default=dict)
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

    def __str__(self) -> str:
        return f"AnalyticByHour for {self.link}"

