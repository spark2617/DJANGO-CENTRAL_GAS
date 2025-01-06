from django.contrib.auth.backends import ModelBackend
from api.models.cliente import Cliente
from api.models.user import CustomUser
from rest_framework import exceptions

class ClienteBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        
        try:
            user = CustomUser.objects.get(telefone=username)
        except CustomUser.DoesNotExist:
            print("Usuário não encontrado")
            raise exceptions.AuthenticationFailed('Não encontramos esse usuario em nossa base de dados')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Usuário não verificado')

        if user.check_password(password):
            print("Senha correta")
            return user
        else:
            print("Senha incorreta")
            raise exceptions.AuthenticationFailed('Senha incorreta')

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
