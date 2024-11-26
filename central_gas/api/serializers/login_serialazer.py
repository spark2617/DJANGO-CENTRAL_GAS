from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Número de telefone ou senha incorretos.")
        
        if not user.is_active:
            raise serializers.ValidationError("Esta conta está desativada.")

        data["user"] = user
        return data
