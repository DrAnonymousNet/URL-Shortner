from yaml import serialize
from ..serializers import LinkSerializer
from .test_base import TestBaseView


class TestSerializer(TestBaseView):

    def test_serializer_valid_data(self):
        valid_data = {
            "long_link":"https://www.django-rest-framework.org/api-guide/testing/#urlpatternstestcase"
        }
        serializer = LinkSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_Serialzer_invalid_data(self):
        invalid_data = {
            "long_link":""
        }
        serializer = LinkSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    

        
