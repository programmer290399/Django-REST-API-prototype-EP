from django.urls import path
from .views import ListCreateDishesView , LoginView , RegisterUsers , DishesDetailView


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('dishes/', ListCreateDishesView.as_view(), name="dishes-list-create"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('dishes/<int:pk>/', DishesDetailView.as_view(), name="dishes-detail")
]






