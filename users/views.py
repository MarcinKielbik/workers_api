from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register new user.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({"error": "Username and password are required"}, 
                        status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Generate JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({"message": "User created successfully", "access_token": access_token}, status=201)
    
    
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Log in user and return token.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    # Genarate JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({"access_token": access_token})
