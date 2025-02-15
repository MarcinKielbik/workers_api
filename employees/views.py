from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Worker
from .serializers import WorkerSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register new User
    """
    
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password:
        return Response({"error": "Username and password are required"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)


    user = User.objects.create_user(username=username, password=password, email=email)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({"message": "User created successfully", "token": token.key}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login user and return token
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def worker_list(request):
    """
    Handles worker list operations.

    - `GET`: Retrieves a list of all workers.
    - `POST`: Creates a new worker or multiple workers at once.
    """
    if request.method == 'GET':
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def worker_detail(request, pk):
    """
    Retrieve a single worker by ID.
    """
    try:
        worker = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist: 
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WorkerSerializer(worker)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def update_worker(request, pk):
    """
    Update a worker's details.

    - `PUT`: Updates all fields of a worker.
    - `PATCH`: Updates specific fields of a worker.
    """
    try:
        worker = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkerSerializer(worker, data=request.data, partial=(request.method == 'PATCH'))
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_worker(request, pk):
    """
        -`DELETE ` Delete worker
    
    """
    try:
        worker = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    worker.delete()
    return Response({'detail': 'Worker deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
