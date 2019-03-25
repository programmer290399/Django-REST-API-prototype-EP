from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Dishes
from .serializers import DishesSerializer


class ListDishesView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer