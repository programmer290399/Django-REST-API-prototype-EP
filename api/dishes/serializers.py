from rest_framework import serializers
from .models import Dishes


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ("name", "restaurant")

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)