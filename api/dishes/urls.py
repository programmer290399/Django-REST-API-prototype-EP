from django.urls import path
from .views import ListDishesView , LoginView , RegisterUsers


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('dishes/', ListDishesView.as_view(), name="dishes-all"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]