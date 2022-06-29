from asyncore import write
from pyexpat import model
from re import A
from rest_framework.routers import reverse
from urllib import request
from rest_framework import serializers
from .models import Link
from .hash_generator import random_md5
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework import status

class AvailableAlready(APIException):
    status_code = status


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model= User
        fields = [
            "username",
            "password",
            "confirm_password"
        ]


    def validate(self, validated_data):
        password = validated_data["password"]
        confirm_password = validated_data["confirm_password"]
        username = validated_data["username"]
        if password != confirm_password:
            raise serializers.ValidationError({"password":"Password must match","confirm_password":"Password must match"}, code="unmatch-password")
        user = User.objects.filter(username=username).exists()
        if user:
            raise serializers.ValidationError({"username":"Usermame already exist"})
        
        return validated_data


    
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        with transaction.atomic():
            user = User.objects.create(username=username, password=password)
            token = Token.objects.create(user=user)
           
            
        return user



class LinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
                  "url",
                  "id",
                  "short_link",
                  "long_link",
                  "last_visited_date",
                  "visit_count",
                  ]

    def create(self, validated_data):
        request = self.context.get("request")

        long_link = validated_data["long_link"]
        link = Link.objects.filter(owner=request.user, long_link=long_link)
        if link.exist():
            return serializers.

        scheme = request.is_secure() and "https" or "http"
        validated_data["short_link"] =  f'{scheme}://{request.get_host()}/{random_md5(long_link)[0]}'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        long_link = validated_data["long_link"]
        validated_data["short_link"] = f"{request.get_host()}/{random_md5(long_link)[0]}"
        return super().update(instance, validated_data)

    def get_url(self, obj):

        request = self.context.get("request")
        base_url = request.get_host()
        url = reverse("link-detail", kwargs={"pk":obj.id})
        scheme = request.is_secure() and "https" or "http"

        full_url = f'{scheme}://{base_url}{url}'
        return full_url

