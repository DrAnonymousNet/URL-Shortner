from .models import Link
import schedule, time


def clean_stale():
    stale = Link.objects.find_stale()
    stale.delete()
    print("Wahooooo")


schedule.every().day.at("21:25").do(clean_stale)

