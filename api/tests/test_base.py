import email
from django.test import Client, TestCase
from django.urls import include, path
from requests import request
from rest_framework.routers import reverse
from rest_framework.test import APIRequestFactory,APISimpleTestCase,APITestCase, URLPatternsTestCase
from django.contrib.auth import get_user_model
from api.models import Link
User = get_user_model()


class TestBaseView(APITestCase):
    def setUp(self) -> None:
        urlpatterns = [
            path("", include("url_shortner.urls"))
        ]
   
        self.request = APIRequestFactory()
        self.client = Client()
        self.user = User.objects.create(email="test@gmail.com",
                                        password="12345")
        
        self.link_1 = Link.objects.create(long_link="https://stackoverflow.com/questions/23467032/how-to-set-up-load-balancing-with-nginx-and-gunicorn")
        self.link_2 = Link.objects.create(long_link="https://chat.whatsapp.com/I6P6T9T3Oev3v6LJN6Fc7W")
        self.user.is_active =True

        #self.link_list_url = reverse("link-list")

        #self.link_detail_url = reverse("link-detail", kwargs={"id":1})

        
        self.client.login(email="test@gmail.com", password = "12345")
        return super().setUp()