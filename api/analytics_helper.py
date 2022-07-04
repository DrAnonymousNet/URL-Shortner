import os
from pytz import country_names
from django.contrib.gis.geoip2 import GeoIP2
from django_user_agents.utils import get_user_agent
from geoip2.errors import AddressNotFoundError
from datetime import datetime, timedelta
from django.db import transaction, models
from .models import Analytic, AnalyticByDateTime


from django.db.models import F, Func, Value, JSONField



def update_analytic(request, link):
    analytic = link.analytic
    with transaction.atomic():
        user_agent = get_user_agent(request)
        update_country_analytic(request, analytic)
        update_device_analytic(user_agent, analytic)
        update_date_time_analytic(request, link)
        analytic.save()
        link.save()
        
        #updated_analytic.country.setdefault(country_name, #country_count
    
    return True
    

def update_date_time_analytic(request, link):
    date_time = datetime.now()
    analytic = link.analyticbydatetime_set
    try:
        curr = analytic.get(date=date_time.date(), time__hour=date_time.time().hour)
    except:
        analytic.create(date=str(date_time.date()), time=date_time.time(), count=1)
        return 
    curr.count = models.F("count") + 1
    curr.save()
    return

def update_device_analytic(user_agent, analytic)-> bool:
    _os = user_agent.get_os()
    _device = user_agent.get_device()
    _browser = user_agent.get_browser()
    _os = user_agent.get_os()
    device_count = analytic.device.setdefault(_device ,0)
    analytic.device.update({_device:device_count+1})
    browser_count = analytic.browser.setdefault(_browser, 0)
    analytic.browser.update({_browser:browser_count+1})
    os_count = analytic.os.setdefault(_os, 0)
    analytic.os.update({_os:os_count+1})
    return True
  

def update_country_analytic(request,analytic)->bool:
    country_name = GetCountryData(request)
    country_count =analytic.country.setdefault(country_name, 0)
    analytic.country.update({country_name:country_count+1})
    return True
   


def GetCountryData(request)-> str:
    ip_address = "197.211.53.16"
    if ip_address:
        try:              
            g = GeoIP2()
            country = g.country_name(ip_address)
        except AddressNotFoundError:
            country = "Others"
    return country


        
def get_start_and_end_date():
    date = datetime.date.today()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)
    return start_week, end_week