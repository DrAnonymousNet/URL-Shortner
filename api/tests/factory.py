import datetime
from unittest import mock
import factory
from api.models import Link
from api.hash_generator import random_md5
from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker("email")


class LinkFactory(factory.Factory):
    class Meta:
        model = Link
        exclude = ("host")

    long_link = factory.Faker("url")
    owner = factory.SubFactory(UserFactory)
    short_link = factory.LazyAttribute(
        lambda _self: random_md5(
            _self.long_link,
            _self.owner.email))
    date_created = factory.Faker("date", end_datetime=datetime.date.today())
    last_visited_date = factory.Faker(
        "date_between_dates",
        date_start=factory.SelfAttribute("..date_created"))

    @factory.lazy_attribute
    def short_link(_self):
        host = config("HOST")
        short = random_md5(_self.long_link, _self.owner.email)
        full_url = f"http://{host}/{short}"
        return full_url
