import logging
from django.contrib.gis.geoip2 import GeoIP2
from django_user_agents.utils import get_user_agent
from geoip2.errors import AddressNotFoundError
from datetime import datetime, timedelta
from django.db import transaction, models
from .models import Analytic, AnalyticByDateTime


from django.db.models import F, Func, Value, JSONField
from url_shortner.celery import app
logger = logging.getLogger("testlogger")

FLAGGED_AGENT = ["FacebookBot", "LinkedlnBot","Go-http-client", "Twitterbot", "TelegramBot"]

@app.task(name="analytic")
def update_analytic(request, link):
    analytic = link.analytic
    with transaction.atomic():
        user_agent = get_user_agent(request)
        status = update_device_analytic(user_agent, analytic)
        if status:
            update_country_analytic(request, analytic)
            update_referer_analyic(request, analytic)
            update_date_time_analytic(request, link)
            analytic.save()
            link.save()
        else:
            return False
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
    _browser = user_agent.get_browser().split(" ")[0]

    if _browser in FLAGGED_AGENT:
        logger.info(_browser)
        return False
    logger.info("This Were ALLOWED")
    logger.info(_browser)
    _device = user_agent.get_device().split(" ")[0]
    _os = user_agent.get_os().split(" ")[0]
    device_count = analytic.device.setdefault(_device ,0)
    analytic.device.update({_device:device_count+1})
    browser_count = analytic.browser.setdefault(_browser, 0)
    analytic.browser.update({_browser:browser_count+1})
    os_count = analytic.os.setdefault(_os, 0)
    analytic.os.update({_os:os_count+1})
    return True
  
def update_referer_analyic(request, analytic):
    _referer = request.META.get("HTTP_REFERER")
    if _referer:
        referer_count = analytic.referer.setdefault(_referer, 0)
        analytic.referer.update({_referer:referer_count+1})


def update_country_analytic(request,analytic)->bool:
    country_name = GetCountryData(request)
    country_count =analytic.country.setdefault(country_name, 0)
    analytic.country.update({country_name:country_count+1})
    return True
   


def GetCountryData(request)-> str:
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    country = ""
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