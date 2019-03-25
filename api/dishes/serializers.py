from rest_framework import serializers
from .models import Dishes


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ("name", "restaurant")