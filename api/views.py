from django.shortcuts import render
import json
from rest_framework import generics, status
from .serializers import (
    UserSerializer,
    OrdersSerializer,
    UploadedFileSerializer,
)
from .models import Orders, CustomUser, UploadedFile
from django.db import models
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
from django.http import JsonResponse, FileResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@csrf_exempt
@api_view(['POST'])
def send_registration_email(request):
    name = request.data['name']
    militar_idt = request.data['militar_idt']
    email = request.data['email']
    is_field_operator = request.data['field_operator']
    is_base_operator = request.data['base_operator']
    is_admin = request.data['admin']
    comments = request.data['comments']
    # Create the email message
    message = f'''
    Nome Completo: {name}
    Nº Idt Mil: {militar_idt}
    E-mail: {email}
    Operador de campo: {is_field_operator}
    Operador de base: {is_base_operator}
    Administrador: {is_admin}
    Comentários: {comments}

    Para autenticar esse usuário, clique no link: http://localhost:3000/login
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

@api_view(['PUT'])
def update_order_status(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Check if the request contains a 'status' field in the JSON data
        if 'status' in request.data:
            new_status = request.data['status']
            operator_comments = request.data['operator_comments']
            # Check if the new_status is valid (e.g., 'Aprovado' or 'Reprovado')
            if new_status in ['Aprovado', 'Reprovado']:
                order.status = new_status
                order.operator_comments = operator_comments
                order.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Status field is missing in the request data'}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
def operators(request):
    # Retrieve the list of base operators from the CustomUser table
    operators = CustomUser.objects.all()
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

@api_view(['GET'])
def get_orders(request, id):
    if id is not None:
        # Query for orders where either base_operator or field_operator matches the provided operator_id
        orders =  Orders.objects.filter(
                base_operator=id
            ) | Orders.objects.filter(
                field_operator=id
            )

        # Serialize the orders' data
        orders_serializer = OrdersSerializer(orders, many=True)

        return Response(orders_serializer.data)
    else:
        return Response({'detail': 'Operator ID not provided in headers'}, status=400)
    
@api_view(['DELETE'])
@csrf_exempt
def delete_order(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
        order.delete()
        return JsonResponse({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Orders.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_file(request, id):
    if id is not None:
        file =  UploadedFile.objects.filter(id=id)

        file_serializer = UploadedFileSerializer(file, many=True)

        return Response(file_serializer.data[0]['file'])
    else:
        return Response({'detail': 'Operator ID not provided in headers'}, status=400)
  
@api_view(['GET'])  
def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    response = FileResponse(uploaded_file.file, as_attachment=True)
    return response

@api_view(['GET'])
def get_orders_by_order_id(request, order_id):
    if order_id is not None:
        # Query for orders where either base_operator or field_operator matches the provided operator_id
        orders =  Orders.objects.filter(id=order_id)

        # Serialize the orders' data
        orders_serializer = OrdersSerializer(orders, many=True)

        return Response(orders_serializer.data)
    else:
        return Response({'detail': 'Order ID not provided in headers'}, status=400)

class OrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class UsersView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UploadedFileView(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
