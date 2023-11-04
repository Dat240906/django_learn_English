from rest_framework import serializers
from .models import *





class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=12)
    password = serializers.CharField(max_length=12)