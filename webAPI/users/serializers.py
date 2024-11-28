from rest_framework import serializers
from .models import User, WishListItem
from django.contrib.auth import authenticate

class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = ['id', 'name', 'image', 'price', 'mercado_libre_url']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'phone', 'gender', 'role', 'state')
        extra_kwargs = {'password': {'write_only': True}}
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'last_name', 'email', 'phone', 'gender', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = User(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.state:
                    raise serializers.ValidationError('Usuario inactivo.')
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError('Credenciales incorrectas.')
        else:
            raise serializers.ValidationError('Debe proporcionar "username" y "password".')