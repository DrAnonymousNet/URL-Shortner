from datetime import datetime, tzinfo
from pytz import timezone
from rest_framework.routers import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Link
from .hash_generator import random_md5,build_full_url
from django.db import transaction
from rest_framework.authtoken.models import Token
from .exceptions import *
from dateutil import tz
from datetime import datetime

User = get_user_model()



class LinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    analytic = serializers.SerializerMethodField()
    class Meta:
        model = Link
        fields = [
                  "url",
                  "id",
                  "owner",
                  "short_link",
                  "long_link",
                  "date_created",
                  "last_visited_date",
                  "visit_count",
                  'analytic'
                  ]
        extra_kwargs = {"owner":{
            "read_only":True,}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        long_link = validated_data["long_link"]
        user = request.user if request.user.is_authenticated else None
        link = Link.objects.filter(owner=user, long_link=long_link)
        if link.exists():
            raise AvailableAlready({"message":"link already exist", "short_link":link.first().short_link})
        base_url = build_full_url(request)
        validated_data["short_link"] =  f'{base_url}/{random_md5(long_link, user)}'
    
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        long_link = validated_data["long_link"]
        validated_data["short_link"] = f"{request.get_host()}/{random_md5(long_link, instance.owner)}"
        return super().update(instance, validated_data)

    def get_url(self, obj):
        request = self.context.get("request")
        url = reverse("link-detail", request=request, kwargs={"pk":obj.id})
        return url

    def get_owner(self, obj):
        if obj.owner is None:
            return None
        return obj.owner.email

    def get_analytic(self, obj):
        obj_analytic = obj.analyticbydatetime_set
        
        analytic = {"date_time_anaylytic":obj_analytic.get_analytic(obj),
                     "other_analytic": {"Browser": obj.analytic.browser,
                                        "OS":obj.analytic.os,
                                        "Device":obj.analytic.device,
                                        "Referer":obj.analytic.referer,
                                        "Country":obj.analytic.country
                                        }   
        }
        return analytic

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        long_link = data.get("long_link")
        try:
            tzinfo = User.objects.get(email=data.get("owner")).timezone 
        except:
            tzinfo = "UTC"
        date_created =data.get("date_created")
        last_visited_date = data.get("last_visited_date")
        usertzinfo = tz.gettz(tzinfo)

        date_created = change_to_owner_tz(date_created, usertzinfo)
        last_visited_date = change_to_owner_tz(last_visited_date, usertzinfo)
        print(long_link, "\n", len(long_link))
        #if len(long_link) > 255:
        #    raise LinkTooLong({"error":"Link cannot be greater than 255"})

        return data

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        try:
            tzinfo = User.objects.get(email=instance.get("owner")).timezone 
        except:
            tzinfo = "UTC"
        usertzinfo = tz.gettz(tzinfo)
        date_created =instance.get("date_created")
        last_visited_date = instance.get("last_visited_date")
        date_created = change_to_owner_tz(date_created, usertzinfo)
        print(last_visited_date)
        last_visited_date = change_to_owner_tz(last_visited_date, usertzinfo)
        instance["date_created"] = str(date_created)
        instance["last_visited_date"] = last_visited_date if last_visited_date == None else str(last_visited_date)
        return instance

def change_to_owner_tz(date, tz):
    if date == "None" or date == None:
        return date
    try:
        create_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        create_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")

    date_with_tz = create_date.astimezone(tz=tz)
    return date_with_tz




'''
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

'''

