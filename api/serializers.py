
from rest_framework.routers import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Analytic, Link
from .hash_generator import random_md5
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework import status

class AvailableAlready(APIException):
    status_code = status.HTTP_208_ALREADY_REPORTED


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
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Link
        fields = [
                  "url",
                  "id",
                  "owner",
                  "short_link",
                  "long_link",
                  "last_visited_date",
                  "visit_count",
                  ]
        extra_kwargs = {"owner":{
            "read_only":True,
        }
        
        }

    def create(self, validated_data):
        request = self.context.get("request")

        long_link = validated_data["long_link"]
        user = request.user if request.user.is_authenticated else None
        link = Link.objects.filter(owner=user, long_link=long_link)
        if link.exists():
            raise AvailableAlready({"message":"link already exist", "short_link":link.first().short_link})

        scheme = request.is_secure() and "https" or "http"
        validated_data["short_link"] =  f'{scheme}://{request.get_host()}/{random_md5(long_link, user)[0]}'
    
        return super().create(validated_data)

    def update(self, instance, validated_data):
    
        request = self.context.get("request")
        long_link = validated_data["long_link"]
        validated_data["short_link"] = f"{request.get_host()}/{random_md5(long_link, instance.owner)[0]}"
        return super().update(instance, validated_data)

    def get_url(self, obj):

        request = self.context.get("request")
        url = reverse("link-detail", request=request, kwargs={"pk":obj.id})
        return url

    def get_owner(self, obj):
        if obj.owner is None:
            return None
        return obj.owner.username

