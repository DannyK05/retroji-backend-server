from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"message": "Username and password are required", },
                        status=status.HTTP_400_BAD_REQUEST)
  
    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already taken", },
                        status=status.HTTP_400_BAD_REQUEST)
    
    if email and User.objects.filter(email=email).exists():
        return Response({"message": "Email already taken", },
                    status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    tokens = get_tokens_for_user(user)
    serialized_user = UserSerializer(user)

    return Response({"message": "Account created", "data":{"user": serialized_user.data,}, 'tokens':tokens},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)
        serialized_user = UserSerializer(user)
        return Response({"message": "You are logged in", "data":{"user": serialized_user.data,}, 'tokens':tokens},
                        status=status.HTTP_200_OK)
    
    return Response({"message": "Invalid username or password"},
                    status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    return Response({'message': "Logged out"}, status=status.HTTP_200_OK)