from .backends import ClienteBackend
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    telefone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        telefone = attrs.get('telefone')
        password = attrs.get('password')

        user = ClienteBackend.authenticate(self,username=telefone, password=password)
        if not user:
            raise serializers.ValidationError("Não encontramos esse usuario em nossa base de dados ou a senha está incorreta.")
        
        attrs['user'] = user
        return attrs
