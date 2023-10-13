from ipaddress import ip_address
from rest_framework import serializers
from .models import *



class NoficationsSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1500,required=False)
    type = serializers.CharField(max_length=20)
    user_name = serializers.CharField(max_length=12, required=False)
    ip_address = serializers.IPAddressField(required = False)
    


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=12)
    password = serializers.CharField(max_length=12)