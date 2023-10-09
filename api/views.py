from django.shortcuts import render
import json
from rest_framework import generics, status
from .serializers import (
    UserSerializer,
    OrdersSerializer,
    UserFilesSerializer,
)
from .models import Orders, CustomUser, UserFiles
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
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
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    name = request.data['name']
    idt_mil = request.data['idt_mil']
    password = request.data['password']
    email = request.data['email']
    comments = request.data['comments']
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
@csrf_exempt 
@api_view(['POST'])
def create_user(request):    
    serializer = UserSerializer(data=request.data)

    # Extract user data from the JSON
    name = request.data["name"]
    email = request.data["email"]
    militar_idt = request.data["militar_idt"]
    password = request.data["password"]
    comments = request.data["comments"]
    is_field_operator = request.data["is_field_operator"]
    is_base_operator = request.data["is_base_operator"]
    is_admin = request.data["is_admin"]   
    try:    
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            name=name,
            militar_idt=militar_idt,
            comments=comments,
            field_operator=is_field_operator,
            base_operator=is_base_operator,
            admin=is_admin,
            approved=False,  # Set this as needed
        )
        # Return a success response
        return JsonResponse({"message": "User created successfully"}, status=201)

    except Exception as e:
        # Handle any exceptions that may occur during user creation
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['POST'])
def create_order(request):
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class UsersView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserFilesView(generics.ListCreateAPIView):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
