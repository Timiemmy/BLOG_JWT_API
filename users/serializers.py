from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer class to authenticate users with email and password.
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password',)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        
        raise serializers.ValidationError("Incorrect Credentials")
    

class ProfileSerializer(CustomUserSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = ("bio",)


class ProfileAvatarSerializer(CustomUserSerializer):
    """
    Serializer class to serialize the user Profile avatar
    """

    class Meta:
        model = Profile
        fields = ("avatar",)
