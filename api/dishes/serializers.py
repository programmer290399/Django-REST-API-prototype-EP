from rest_framework import serializers
from .models import Dishes 
from django.contrib.auth.models import User


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ("name", "restaurant")
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.restaurant = validated_data.get("restaurant", instance.restaurant)
        instance.save()
        return instance

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


