from rest_framework import serializers
from .models import CustomUser, Orders, UploadedFile
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError


# PFC Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'militar_idt', 'field_operator', 'base_operator', 'admin', 'approved')


class OrdersSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), many=True)
    class Meta:
        model = Orders
        fields = (
            "id",
            "field_operator",  # Include the field operator name
            "base_operator",  # Include the base operator name
            "datetime_of_sending",
            "files",
            "status",
            "order_name",
            "field_comments",
            "operator_comments",
        )

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ("id", "file", "uploaded_at")
