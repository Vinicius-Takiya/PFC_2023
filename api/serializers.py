from rest_framework import serializers
from .models import CustomUser, Orders, UserFiles
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError


# PFC Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'militar_idt', 'field_operator', 'base_operator', 'admin', 'approved')


class OrdersSerializer(serializers.ModelSerializer):
    field_operator_name = serializers.ReadOnlyField(source='field_operator.name')
    base_operator_name = serializers.ReadOnlyField(source='base_operator.name')

    class Meta:
        model = Orders
        fields = (
            "id",
            "field_operator",
            "field_operator_name",  # Include the field operator name
            "base_operator",
            "base_operator_name",  # Include the base operator name
            "datetime_of_sending",
            "files",
            "status",
            "order_name",
            "field_comments",
            "operator_comments",
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            "field_operator",
            "base_operator",
            "files",
            "order_name",
            "field_comments",
        )


class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFiles
        fields = ("id", "user", "file", "description", "uploaded_at")
