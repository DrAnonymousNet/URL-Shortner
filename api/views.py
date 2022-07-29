from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie


from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from rest_framework.routers import reverse
from rest_framework import viewsets, permissions

from .filters import LinkFilter
from .models import Link
from .serializers import *
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from .analytics_helper import *
from .permissions import isOwner
import logging
from .analytics_helper import is_blacklisted
from dateutil import tz


logger = logging.getLogger("testlogger")


def index(request):
    return render(request, "index.html")


class LinkViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.AllowAny]
    #filterset_fields = ['owner__email', 'visit_count', "date_created", "last_visited_date"]
    filterset_class = LinkFilter
    serializer_class = LinkSerializer
    queryset = Link.objects.all().select_related("analytic","owner").prefetch_related("analyticbydatetime_set")
    http_method_names = ["get", "post", "delete", "patch"]

    @method_decorator(cache_page(15*60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            owner = request.user
        else:
            owner = None
        serializer = LinkSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        instance= serializer.save(owner = owner)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        url = request.build_absolute_uri(reverse("link-detail",request=request, kwargs = {"pk":response.data.get("id")}))
        response.headers["Location"] = url
        return response

    def retrieve(self, request, *args, **kwargs):
        print(kwargs, args)
        return super().retrieve(request, *args, **kwargs)


    def get_permissions(self):
        permission_class = []
        if self.action in ["list"] :
            permission_class += [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action in ["retrieve", "delete", "partial_update"]:
            permission_class += [isOwner()]
        elif self.action in ["create"]:
            permission_class += [permissions.AllowAny()]
        return permission_class


class RedirectView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request:HttpRequest, **kwargs):
        logger.info(request.META)
        short_link = kwargs.get("short_link")
        full_short_link = f"{build_full_url(request)}/{short_link}"
        
        try:
            link = Link.objects.get(short_link=full_short_link)
            print(link.last_visited_date)
            owner = link.owner
        except:
            return Response({"error":"The link cannot be found"}, status=status.HTTP_404_NOT_FOUND)
        if owner:
            tzinfo = tz.gettz(owner.timezone or "UTC")
        else:
            tzinfo = tz.gettz("UTC")

        if not is_blacklisted(request) and update_analytic(request, link, tzinfo):
            link.visit_count = F("visit_count") + 1
            link.last_visited_date = datetime.now(tz=tzinfo or tz.get("UTC"))
            link.save()
        long_link = link.long_link
        
        return redirect(long_link)

    
'''  
class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes= []

    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        user = serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json')
        response.headers["Location"] = ""
        response.data["Token"] = user.auth_token.key
        return response
   ''' 



