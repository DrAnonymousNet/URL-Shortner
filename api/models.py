from statistics import mode
from urllib import request
from django.db import models
from django.utils .translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db.models import F, Q
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from .hash_generator import random_md5

# Create your models here.

User = get_user_model()
 

class LinkManager(models.Manager):

    def find_stale(self):
        return self.annotate(days_of_inactive = F("last_visited_date") - datetime.now().date()).filter(days_of_inactive__gte = timedelta(days = 30))


class Link(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    short_link = models.URLField(_("Short link"), unique=True, editable=False)
    long_link = models.URLField(_("Long link"), blank=False, null=False)
    last_visited_date = models.DateField(_("last visited"), auto_now=True, editable=False)
    visit_count = models.PositiveBigIntegerField(_("visit count"),editable=False, default=0)
    objects = LinkManager()


    def save(self, **kwargs) -> None:
        if not self.short_link:
            self.short_link = f"{request.get_host()}/{random_md5(self.long_link)[0]}"
        return super().save(**kwargs)

    def __str__(self) -> str:
        return self.short_link

    


