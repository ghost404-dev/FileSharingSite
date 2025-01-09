from rest_framework import serializers
from .models import User, File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'file', 'filename', 'upload_at', 'file_type']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2']

    def validate_password(self, value):
        if value != self.initial_data.get('password2'):
            raise serializers.ValidationError('Пароли не совпадают')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user