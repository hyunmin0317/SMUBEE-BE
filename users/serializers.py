# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User


# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")