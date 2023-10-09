from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.db.models import FileField

from django.http import JsonResponse

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You must provide an email address")
        
        print(extra_fields)
        email = self.normalize_email(email)
        comments = extra_fields.pop('comments', '')
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    militar_idt = models.CharField(max_length=30, unique=True)
    field_operator = models.BooleanField(default=True)
    base_operator = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    objects = CustomUserManager()

    # Specify unique related names for groups and user_permissions fields
    groups = models.ManyToManyField(Group, verbose_name='groups', related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', related_name='custom_users')

    def __str__(self):
        return self.email

def user_file_upload_path(instance, filename):
    # Get the user's ID from the session
    user_id = instance.user.id
    # Construct the upload path: 'user_files/user_id/filename'
    return f'user_files/{user_id}/{filename}'

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')    
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    # You can add other fields if needed, such as a description or uploader info

    def __str__(self):
        return self.file.name

class OrdersFile(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)

class Orders(models.Model):
    STATUS_CHOICES = (
        ("Aprovado", "Aprovado"),
        ("Reprovado", "Reprovado"),
        ("Aguardando Análise", "Aguardando Análise"),
    )

    datetime_of_sending = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField(UploadedFile, through=OrdersFile, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Aguardando Análise")
    order_name = models.CharField(max_length=255)
    field_operator = models.BigIntegerField()
    base_operator = models.BigIntegerField()
    field_comments = models.TextField(blank=True)
    operator_comments = models.TextField(blank=True)

    def __str__(self):
        return self.order_name
