from django.urls import path
from .views import ListDishesView , LoginView


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('dishes/', ListDishesView.as_view(), name="dishes-all")
]