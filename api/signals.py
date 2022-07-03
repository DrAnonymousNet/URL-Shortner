from django.dispatch import receiver
from api.models import Analytic, AnalyticByDateTime, Link
from django.db.models.signals import post_save


@receiver(post_save, sender =Link)
def analytic_receiver(sender,instance, **kwargs):
    if kwargs["created"]:
        Analytic.objects.create(link=instance)
        AnalyticByDateTime.objects.create(link=instance)
