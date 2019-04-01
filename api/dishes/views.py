from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from .models import Dishes
from rest_framework.views import status
from .serializers import DishesSerializer , TokenSerializer , UserSerializer
from .decorators import validate_request_data





jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ListCreateDishesView(generics.ListCreateAPIView):
    
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_dish = Dishes.objects.create(
            name=request.data["name"],
            restaurant=request.data["restaurant"]
        )
        return Response(
            data=DishesSerializer(a_dish).data,
            status=status.HTTP_201_CREATED
        )

class DishesDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_dish = self.queryset.get(pk=kwargs["pk"])
            return Response(DishesSerializer(a_dish).data)
        except Dishes.DoesNotExist:
            return Response(
                data={
                    "message": "dish with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_dish = self.queryset.get(pk=kwargs["pk"])
            serializer = DishesSerializer()
            updated_dish = serializer.update(a_dish, request.data)
            return Response(DishesSerializer(updated_dish).data)
        except Dishes.DoesNotExist:
            return Response(
                data={
                    "message": "dish with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_dish = self.queryset.get(pk=kwargs["pk"])
            a_dish.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dishes.DoesNotExist:
            return Response(
                data={
                    "message": "dish with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )




