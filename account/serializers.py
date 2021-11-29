from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    re_password = serializers.CharField(max_length=200)
    
    def validate_new_password(self, value):
        if value != self.initial_data['re_password']:
            raise serializers.ValidationError("Please enter matching passwords")
        return value
    