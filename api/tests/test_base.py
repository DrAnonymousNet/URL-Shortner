import email
from os import access
from django.urls import include, path
from requests import request
from django.urls import reverse_lazy
from rest_framework.routers import reverse
from rest_framework.test import APIRequestFactory,APISimpleTestCase,APITestCase, URLPatternsTestCase, APIClient
from django.contrib.auth import get_user_model
from api.models import Link
from api.views import LinkViewSet
User = get_user_model()


class TestBaseView(APITestCase):
    def setUp(self) -> None:
        urlpatterns = [
            path("", include("url_shortner.urls"))
        ]

        self.client = APIClient()

        self.user = User.objects.create_superuser(email="test@gmail.com",
                                        password="12345") 
        self.user2 = User.objects.create(email="test2@gmail.com",
                                        password="12345")
        self.user.is_active =True
        self.user2.is_active = True

        #Authentication
        JWTToken = self.client.post("/v1/auth/jwt/create", data={"email":"test@gmail.com", "password":"12345"})
        self.access = JWTToken.data["access"]
        self.client.force_authenticate(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.access}")
        
        self.link_1 = Link.objects.create(long_link="https://stackoverflow.com/questions/23467032/how-to-set-up-load-balancing-with-nginx-and-gunicorn", owner=self.user)
        self.link_2 = Link.objects.create(long_link="https://chat.whatsapp.com/I6P6T9T3Oev3v6LJN6Fc7W")
        
        self.link_list_url = "/v1/links/"
        self.link_detail_url = f"/v1/links/{self.link_1.id}"
        
        self.factory = APIRequestFactory()
        
