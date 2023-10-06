from django.db import models
import string
import random

def generate_unique_code():
    lenght = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class UsersManager(models.Manager):
    def field_operators(self):
        return self.filter(permissions='Field Operator')

    def base_operators(self):
        return self.filter(permissions='Base Operator')

class Users(models.Model):
    PERMISSION_CHOICES = (
        ("Field Operator", "Field Operator"),
        ("Base Operator", "Base Operator"),
        ("Admin", "Admin"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    militar_idt = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255, blank=True)
    permissions = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

    def __str__(self):
        return self.name

class UserFiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')  # Set the upload directory as per your requirements
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name

class Orders(models.Model):
    STATUS_CHOICES = (
        ("Aprovado", "Aprovado"),
        ("Reprovado", "Reprovado"),
        ("Aguardando Análise", "Aguardando Análise"),
    )

    field_operator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='field_orders',
        limit_choices_to={'permissions': 'Field Operator'}
    )

    base_operator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='base_orders',
        limit_choices_to={'permissions': 'Base Operator'}
    )

    datetime_of_sending = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField('UserFiles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    order_name = models.CharField(max_length=255)
    field_comments = models.TextField(blank=True)
    operator_comments = models.TextField(blank=True)

    def __str__(self):
        return self.order_name