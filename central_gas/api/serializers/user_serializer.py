from rest_framework import serializers
from api.models.user import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'telefone', 'tipo', 'codigo_verificacao', 'codigo_recuperacao', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']