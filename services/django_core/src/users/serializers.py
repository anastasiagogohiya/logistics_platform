from .models import CustomUser
from rest_framework import serializers


# Не добавлена валидация полей

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'phone', 'avatar',
                  'is_staff', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        'avatar': {'required': False, 'allow_null': True},
                        'phone': {'required': True, 'allow_null': False},
                        'role': {'required': False, 'read_only': True}} # клиент не может поменять роль

    def create(self, validated_data):
        """Создание нового пользователя и хеширование пароля
        о умолчанию роль Клиент"""
        if 'role' not in validated_data:
            validated_data['role'] = CustomUser.Role.CLIENT
        return CustomUser.objects.create_user(**validated_data)


