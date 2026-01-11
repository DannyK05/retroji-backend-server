from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"message": "Username and password are required", "status":status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already taken", "status":status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    serialized_user = UserSerializer(user)

    return Response({"message": "Account created", "data":{"user": serialized_user.data,}, "status": status.HTTP_201_CREATED},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        django_login(request, user)
        serialized_user = UserSerializer(user)
        return Response({"message": "You are logged in", "data":{"user": serialized_user.data,}, "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)
    
    return Response({"message": "Invalid username or password", "status":status.HTTP_401_NOT_FOUND},
                    status=status.HTTP_401_NOT_FOUND)


@api_view(['POST'])
def logout(request):
    django_logout(request)
    return Response({"message": "You are logged out",  "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)