from urllib import request, response
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.routers import reverse
from rest_framework import viewsets, permissions
from .models import Link
from .serializers import *
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from .analytics_helper import *


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

    
    



class LinkViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    filterset_fields = ['owner', 'visit_count']
    serializer_class = LinkSerializer
    queryset = Link.objects.all()
    http_method_names = ["get", "post", "delete", "patch"]

    def list(self, request, *args, **kwargs):
        print(request.META)
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


    '''
    def get_permissions(self):
        permission_class = []
        if self.action in ["list","partial_update","delete","retrieve","destroy"] :
            permission_class = [permissions.IsAuthenticated()]
        return permission_class
    '''


class RedirectView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request:HttpRequest, **kwargs):
        short_link = kwargs.get("str")
        try:
            user = request.user if request.user.is_authenticated else None
            link = Link.objects.get(short_link__contains=short_link)
        except Http404:
            return Response({"error":"The link cannot be found"}, status=status.HTTP_404_NOT_FOUND)
        update_analytic(request, link)
        link.visit_count = F("visit_count") + 1
        link.save()
        long_link = link.long_link
        
        return redirect(long_link)

    

