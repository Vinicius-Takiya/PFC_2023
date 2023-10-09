from django.shortcuts import render
from rest_framework import generics, status
from .serializers import (
    UsersSerializer,
    OrdersSerializer,
    CreateOrderSerializer,
    UserFilesSerializer,
)
from .models import Orders, Users, UserFiles
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@csrf_exempt
@api_view(['POST'])
def send_registration_email(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    name = request.data['name']
    idt_mil = request.data['idt_mil']
    password=request.data['password']
    email = request.data['email']
    comments = request.data['comments']
    user = User.objects.create(
        username=request.data['email'],  # You can use the email as the username
        email=request.data['email'], 
        password=request.data['password'],  # This should be hashed, not plain text
        )
    user.set_password(request.data['password'])
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    # Create the email message
    message = f'''
    Nome Completo: {name}
    Nº Idt Mil: {idt_mil}
    E-mail: {email}
    Comentários: {comments}
    '''

    # Send the email
    try:
        send_mail(
            'Cadastro Solicitado',
            message,
            'vinicius.takiya@ime.eb.br',  # From email
            ['vinicius.takiya@ime.eb.br'],  # To email
            fail_silently=False,
        )
        return JsonResponse({'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'Error sending email: {str(e)}'}, status=500)

# My project views
@api_view(['POST'])
def signup(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.create(
            username=request.data['email'],  # You can use the email as the username
            email=request.data['email'],
            password=request.data['password'],  # This should be hashed, not plain text
        )
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['email'])  # Assuming you use email as the username
    except User.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(request.data['password']):
        return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsersSerializer(user)

    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        queryset = Orders.objects.all()

        return queryset

@api_view(['POST'])
def create_order(request):
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOrderView(APIView):
    serializer_class = CreateOrderSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()

        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


class UsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class UserFilesView(generics.ListCreateAPIView):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
