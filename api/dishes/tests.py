from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Dishes
from .serializers import DishesSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_dish(name="", restaurant=""):
        if name != "" and restaurant != "":
            Dishes.objects.create(name=name, restaurant=restaurant)

    def setUp(self):
        # add test data
        self.create_dish("Chilli paneer", "Aroma Restaurant")
        self.create_dish("Butter Chicken", "CKD")
        self.create_dish("Masala Dosa", "ICH")
        self.create_dish("cheese sandwhich", "tinkus")


class GetAllDishesTest(BaseViewTest):

    def test_get_all_Dishes(self):
        """
        This test ensures that all Dishes added in the setUp method
        exist when we make a GET request to the Dishes/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("dishes-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Dishes.objects.all()
        serialized = DishesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# Create your tests here.
