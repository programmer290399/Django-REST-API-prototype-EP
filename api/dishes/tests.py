from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Dishes
from .serializers import DishesSerializer , TokenSerializer
from django.contrib.auth.models import User
import json

# Test for models
class DishesModelTest(APITestCase):
    def setUp(self):
        self.a_dish = Dishes.objects.create(
            name="Chilli paneer",
            restaurant="CKD"
        )

    def test_song(self):
        """"
        This test ensures that the dish created in the setup
        exists
        """
        self.assertEqual(self.a_dish.name, "Chilli paneer")
        self.assertEqual(self.a_dish.restaurant, "CKD")
        self.assertEqual(str(self.a_dish), "Chilli paneer - CKD")



# tests for views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_dish(name="", restaurant=""):
        if name != "" and restaurant != "":
            Dishes.objects.create(name=name, restaurant=restaurant)

    def make_a_request(self, kind="post", **kwargs):

        if kind == "post":
            return self.client.post(
                reverse(
                    "dishes-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "dishes-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None
    
    
    def fetch_a_dish(self, pk=0):
        return self.client.get(
            reverse(
                "dishes-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )
    
    def delete_a_dish(self, pk=0):
        return self.client.delete(
            reverse(
                "dishes-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    
    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token
    
    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )


    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        # add test data
        self.create_dish("Chilli paneer", "Aroma Restaurant")
        self.create_dish("Butter Chicken", "CKD")
        self.create_dish("Masala Dosa", "ICH")
        self.create_dish("cheese sandwhich", "tinkus")
        self.valid_data = {
            "name": "test dish",
            "restaurant": "test restaurant"
        }
        self.invalid_data = {
            "name": "",
            "restaurant": ""
        }
        self.valid_dish_id = 1
        self.invalid_dish_id = 100


class GetAllDishesTest(BaseViewTest):

    def test_get_all_Dishes(self):
        """
        This test ensures that all Dishes added in the setUp method
        exist when we make a GET request to the Dishes/ endpoint
        """
        # invoke self.login_client method
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("dishes-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Dishes.objects.all()
        serialized = DishesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetASingleDishesTest(BaseViewTest):

    def test_get_a_dish(self):
        """
        This test ensures that a single dish of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_a_dish(self.valid_dish_id)
        # fetch the data from db
        expected = Dishes.objects.get(pk=self.valid_dish_id)
        serialized = DishesSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a dish that does not exist
        response = self.fetch_a_dish(self.invalid_dish_id)
        self.assertEqual(
            response.data["message"],
            "dish with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AddDishesTest(BaseViewTest):

    def test_create_a_dish(self):
        """
        This test ensures that a single dish can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "Both name and restaurant are required to add a dish"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateDishesTest(BaseViewTest):

    def test_update_a_dish(self):
        """
        This test ensures that a single dish can be updated. In this
        test we update the second dish in the db with valid data and
        the third dish with invalid data and make assertions
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=3,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "Both name and restaurant are required to add a dish"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class DeleteDishesTest(BaseViewTest):

    def test_delete_a_dish(self):
        """
        This test ensures that when a dish of given id can be deleted
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.delete_a_dish(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test with invalid data
        response = self.delete_a_dish(100)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """
    def test_register_a_user(self):
        response = self.register_a_user("new_user", "new_pass", "new_user@mail.com")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

