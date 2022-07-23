import logging
from re import U
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
        not_is_robot = update_device_analytic(user_agent, analytic)
        ip_not_crawler = update_country_analytic(request, analytic)

        if not_is_robot and ip_not_crawler:
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
    _browser:str = get_browser(user_agent)
    if _browser in FLAGGED_AGENT or "bot" in _browser.lower():
        #logger.info(_browser)
        return False
    #logger.info(_browser)
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
    countries = ["canada", "united states", "sweden", "finland", "united kingdom"]
    referer = request.META.get("HTTP_REFERER")

    country_name = GetCountryData(request)
    if country_name.lower() in countries and referer== "https://t.co/":
        return False
    country_count =analytic.country.setdefault(country_name, 0)
    analytic.country.update({country_name:country_count+1})
    return True
   


def GetCountryData(request)-> str:
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    country = ""
    if ip_address:
        try:              
            g = GeoIP2()
            print(ip_address)
            country = g.country_name(ip_address)
        except AddressNotFoundError:
            country = "Others"
    return country


        
def get_start_and_end_date():
    date = datetime.date.today()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)
    return start_week, end_week

def is_blacklisted(request):
    RAW_URI = request.META.get("RAW_URI")
    if "robot" in RAW_URI.lower():
        return True
    return False

def get_browser(user_agent):
    _browser:str = user_agent.get_browser().split(" ")
    if len(_browser) > 2:
        _browser = " ".join(_browser[:2])
    else:
        _browser = _browser[0]

    return _browser