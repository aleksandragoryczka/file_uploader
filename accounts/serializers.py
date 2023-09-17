from dj_rest_auth import serializers
from rest_framework.fields import IntegerField
from rest_framework.serializers import CharField


class LoginSerializer(serializers.LoginSerializer):
    email = None
    #password = None


