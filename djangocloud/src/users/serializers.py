import re
from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class UsersSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], max_length=255
    )
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'age', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        return super().update(instance, validated_data)