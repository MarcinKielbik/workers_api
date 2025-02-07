from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Worker
from .serializers import WorkerSerializer

@api_view(['GET', 'POST'])
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
