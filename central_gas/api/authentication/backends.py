from django.contrib.auth.backends import ModelBackend
from api.models.cliente import Cliente
from rest_framework import exceptions

class ClienteBackend(ModelBackend):


    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            
            user = Cliente.objects.get(telefone=username)
        except Cliente.DoesNotExist:
            raise exceptions.AuthenticationFailed('Não encontramos esse usuario em nossa base de dados')

       
        if user.check_password(password):
            return user
        else:
            raise exceptions.AuthenticationFailed('Senha incorreta')

    def get_user(self, user_id):
        try:
            return Cliente.objects.get(pk=user_id)
        except Cliente.DoesNotExist:
            return None
            
