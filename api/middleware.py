from django.conf import settings
from . import models

def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.request = request
        response = get_response(request)
        return response

    return middleware

class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"

        return response