from urllib import request, response
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import viewsets, permissions
from .models import Link
from .serializers import *
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F



class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes= []

    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.headers["Location"] = ""
        response.data["Token"] = user.auth_token.key
        return response

    
    



class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            owner = request.user
        else:
            owner = None
        serializer = LinkSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner = owner)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        url = request.build_absolute_uri(reverse("link-detail", kwargs = {"pk":response.data.get("id")}))
        response.headers["Location"] = url
        return response

    

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            qs = user.link_set.all()
            return qs
        return super().get_queryset()
    
    def get_permissions(self):
        permission_class = []
        if self.action in ["list","partial_update","delete","retrieve"] :
            permission_class = [permissions.IsAuthenticated()]
        return permission_class

    def get_serializer_context(self):
        context =  super().get_serializer_context()

        context["request"] = self.request
        return context


class RedirectView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request:HttpRequest, **kwargs):
        short_link = kwargs.get("str")
        try:
            
            link = Link.objects.get(short_link__contains=short_link)
        except Http404:
            return Response({"error":"The link cannot be found"}, status=status.HTTP_404_NOT_FOUND)
        link.visit_count = F("visit_count") + 1
        link.save()
        long_link = link.long_link
        redirect(long_link)
        return Response({"status":"Redirect successful"}, status=status.HTTP_308_PERMANENT_REDIRECT)

