from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer, UsersSerializer, OrdersSerializer, UserFilesSerializer
from .models import Room, Orders, Users, UserFiles

# Create your views here.
class RoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
class OrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class UsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserFilesView(generics.ListCreateAPIView):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer