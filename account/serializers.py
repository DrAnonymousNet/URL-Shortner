from select import select
from djoser.serializers import UserCreateSerializer
from pytz import timezone


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields
        print(fields)
        fields += ["timezone"]
