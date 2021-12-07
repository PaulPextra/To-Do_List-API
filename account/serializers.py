from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 
                  'last_name', 
                  'username', 
                  'email', 
                  'phone', 
                  'gender',
                  'address', 
                  'password', 
                  'is_active', 
                  'date_joined']

class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    gender = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=200)
    is_active = serializers.BooleanField(default=True)
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    re_password = serializers.CharField(max_length=200)
    
    def validate_new_password(self, value):
        if value != self.initial_data['re_password']:
            raise serializers.ValidationError("Please enter matching passwords")
        return value
    