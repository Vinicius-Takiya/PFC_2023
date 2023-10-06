from rest_framework import serializers
from .models import Room, Users, Orders, UserFiles

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                              'votes_to_skip', 'created_at')
        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'email', 'militar_idt', 'password',
                              'permissions')
        
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'field_operator', 'base_operator', 'datetime_of_sending', 'files', 
                  'status', 'order_name', 'field_comments', 'operator_comments')
        
class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFiles
        fields = ('id', 'user', 'file', 'description', 'uploaded_at')