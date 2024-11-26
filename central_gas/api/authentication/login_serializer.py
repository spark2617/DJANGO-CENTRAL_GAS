from rest_framework import serializers
from api.models.cliente import Cliente

class LoginSerializer(serializers.Serializer):
    telefone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
