from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Link)
admin.site.register(Analytic)
admin.site.register(AnalyticByDateTime)
admin.site.register(TotalRedirection)
