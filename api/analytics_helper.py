import logging
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpRequest
from django_user_agents.utils import get_user_agent
from datetime import datetime, timedelta, tzinfo
from django.db import transaction, models
from typing import List, Tuple

from django.utils import timezone
from .models import Analytic, Link
from url_shortner.celery import app


logger = logging.getLogger("testlogger")

FLAGGED_AGENT = [
    "FacebookBot",
    "LinkedlnBot",
    "Go-http-client",
    "Twitterbot",
    "TelegramBot"]


@app.task(name="analytic")
def update_analytic(request: HttpRequest, link: Link, tzinfo: tzinfo) -> bool:
    analytic = link.analytic
    with transaction.atomic():
        user_agent = get_user_agent(request)
        not_is_robot = update_device_analytic(user_agent, analytic)
        ip_not_crawler = update_country_analytic(request, analytic)

        if not_is_robot and ip_not_crawler:
            update_referer_analyic(request, analytic)
            update_date_time_analytic(request, link, tzinfo)
            analytic.save()
            # link.save()
        else:
            return False
    return True


def update_date_time_analytic(request, link: Link, tzinfo: tzinfo) -> None:
    date_time = datetime.now(tz=tzinfo)
    analytic = link.analyticbydatetime_set
    try:
        curr = analytic.get(
            date=date_time.date(),
            time__hour=date_time.time().hour)
    except BaseException:
        analytic.create(
            date=str(
                date_time.date()),
            time=date_time.time(),
            count=1)
        return
    curr.count = models.F("count") + 1
    curr.save()
    return


def update_device_analytic(user_agent, analytic: Analytic) -> bool:
    browser: str = get_browser(user_agent)
    if browser in FLAGGED_AGENT or "bot" in browser.lower():
        return False
    # logger.info(_browser)
    device = user_agent.get_device().split(" ")[0]
    os = user_agent.get_os().split(" ")[0]
    device_count = analytic.device.setdefault(device, 0)
    analytic.device.update({device: device_count + 1})
    browser_count = analytic.browser.setdefault(browser, 0)
    analytic.browser.update({browser: browser_count + 1})
    os_count = analytic.os.setdefault(os, 0)
    analytic.os.update({os: os_count + 1})
    return True


def update_referer_analyic(request, analytic) -> None:
    referer = request.META.get("HTTP_REFERER")
    user_agent = get_user_agent(request)
    browser = get_browser(user_agent)
    if browser.lower() == "whatsapp" and not referer:

        referer = "WhatsApp"
    if referer:
        referer_count = analytic.referer.setdefault(referer, 0)
        analytic.referer.update({referer: referer_count + 1})


def update_country_analytic(request, analytic) -> bool:
    countries = [
        "canada",
        "united states",
        "sweden",
        "finland",
        "united kingdom"]
    referer = request.META.get("HTTP_REFERER")

    country_name = GetCountryData(request)
    if country_name.lower() in countries and referer == "https://t.co/":
        return False
    country_count = analytic.country.setdefault(country_name, 0)
    analytic.country.update({country_name: country_count + 1})
    return True


def GetCountryData(request) -> str:
    ip_address: str = request.META.get("HTTP_X_FORWARDED_FOR", "none")
    ip_list: List = ip_address.split(", ")
    if len(ip_list) > 1:
        ip_address = ip_list[0]
    country = ""
    if ip_address:
        try:
            g = GeoIP2()
            country = g.country_name(ip_address)
            if len(ip_list) > 1:
                country_2 = g.country_name(ip_list[1])
                print(country, country_2)

        except BaseException:
            country = "Others"
    return country


def get_start_and_end_date() -> Tuple:
    date = datetime.date.today()
    start_week = date - timedelta(date.weekday())
    end_week = start_week + timedelta(7)
    return start_week, end_week


def is_blacklisted(request) -> bool:
    RAW_URI = request.META.get("RAW_URI", "none")
    if "robot" in RAW_URI.lower():
        return True
    return False


def get_browser(user_agent) -> str:
    browser: str = user_agent.get_browser().split(" ")
    if len(browser) > 2 and isinstance(browser, List):
        browser = " ".join(browser[:2])
    else:
        browser = browser[0]

    return browser
