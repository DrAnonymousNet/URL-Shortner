from statistics import mode
from django.db import models
from django.utils .translation import gettext as _
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class URL(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    short_link = models.URLField(_("Short link"), unique=True, editable=False)
    long_link = models.URLField(_("Long link"), blank=False, null=False)
    last_visited = models.DateField(_("last visited"), auto_now=True, editable=False)
    visit_count = models.PositiveBigIntegerField(_("visit count"),editable=False, default=0)

    def __str__(self) -> str:
        return self.short_link

    


