from django.shortcuts import render
import json
from rest_framework import generics, status
from .serializers import (
    UserSerializer,
    OrdersSerializer,
    UploadedFileSerializer,
)
from .models import Orders, CustomUser, UploadedFile
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
def login(request):
    user = get_object_or_404(CustomUser, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("Senha está errada", status=status.HTTP_404_NOT_FOUND)
    try:
        token = Token.objects.get_or_create(user=user)
    except:
        token = user.auth_token
    serializer = UserSerializer(user)
    return Response({'token': token[0].key, 'user': serializer.data})

@api_view(['GET'])
def get_authenticated_user(request):
    user = request.user  # The authenticated user
    # You can serialize and return user data as needed
    data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        # Add other fields as needed
    }
    return Response(data)

@api_view(['GET'])
def base_operators(request):
    # Retrieve the list of base operators from the CustomUser table
    operators = CustomUser.objects.filter(base_operator=True)
    # Serialize the operators' data as needed
    serialized_operators = [
        {
            'id': operator.id,
            'name': operator.name,
            # Add other fields as needed
        }
        for operator in operators
    ]
    return Response(serialized_operators)

@api_view(['POST'])
def create_order(request):
    # Create a list to store the UploadedFile instances
    file_pks = []
    # Create a list to store the UploadedFile instances
    uploaded_files = []

    data = request.data.copy()  
    # Get the list of uploaded files
    files = request.FILES.getlist('files')
    for file in files:
        uploaded_file = UploadedFile(file=file)
        uploaded_file.save()        
        file_pks.append(uploaded_file.pk)
    del data['files']
    # Create the Orders instance and associate the uploaded files
    orders_serializer = OrdersSerializer(data=data)
    if orders_serializer.is_valid():
        orders = orders_serializer.save()
        for file_pk in file_pks:
            try:
                uploaded_file = UploadedFile.objects.get(pk=file_pk)
                uploaded_files.append(uploaded_file)
                orders.files.add(uploaded_file)
            except UploadedFile.DoesNotExist:
                # Handle the case where the uploaded file with the given pk doesn't exist
                pass
        return Response(status=status.HTTP_201_CREATED)
    return Response(orders_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class UsersView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UploadedFileView(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
