
from urllib import response
from rest_framework.test import APITestCase, URLPatternsTestCase, force_authenticate
from rest_framework.routers import reverse
from ..views import LinkViewSet 
from django.urls import include, path, resolve
from .test_base import TestBaseView

class TestView(TestBaseView):
    

    def test_list_end_point(self):
        response = self.client.get("/v1/links/")
        
        self.assertEqual(response.status_code, 200)

    def test_create_endpoint(self):
        valid_data ={
            "long_link":"https://docs.djangoproject.com/en/1.10/topics/testing/tools/"
        }
        response = self.client.post(self.link_list_url, data=valid_data)
        data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["owner"], self.user.email)
        self.assertEqual(data["visit_count"],0)
        self.assertEqual(data["last_visited_date"], None)
        response = self.client.post(self.link_list_url, data=valid_data)
        self.assertEqual(response.status_code, 208)

 
    def test_patch_endpoint(self):
        initial_short_link = self.link_1.short_link
        response = self.client.patch(self.link_detail_url, data={"long_link":"https://www.django-rest-framework.org/api-guide/testing"}, follow=True)
        self.link_1.refresh_from_db
        
        self.assertEquals(response.status_code, 200)
        print(self.link_1.long_link)
        self.assertTrue(initial_short_link != self.link_1.short_link)
        self.assertEqual(self.last_visited_date, None)

    def test_delete_endpoint(self):
        response = self.client.delete(self.link_detail_url, follow=True)
        print(response)
        self.assertEqual(response.status_code, 200)





        



    #def test_link_detail_url(self):
        #self.assertEquals(resolve(self.link_detail_url).func.view_class,LinkViewSet)
    
