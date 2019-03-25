from django.urls import path
from .views import ListDishesView

urlpatterns = [
    path('dishes/', ListDishesView.as_view(), name="dishes-all")
]