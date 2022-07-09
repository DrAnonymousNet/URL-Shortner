from rest_framework.test import APITestCase, URLPatternsTestCase
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
        response = self.client.post("/v1/links/", data=valid_data, request=self.request)
        data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["owner"], None)
        self.assertEqual(data["visit_count"],0)
        self.assertEqual(data["last_visited_date"], None)
        response = self.client.post("/v1/links/", data=valid_data, request=self.request)
        print(response)

        self.assertEqual(response.status_code, 208)



        



    #def test_link_detail_url(self):
        #self.assertEquals(resolve(self.link_detail_url).func.view_class,LinkViewSet)
    
