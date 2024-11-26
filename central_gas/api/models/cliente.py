from django.db import models
from .endereco import Endereco
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from api.service.enviar_mensagem_whatsapp import enviar_mensagem_wppconnect
import random

class ClienteManager(BaseUserManager):

    def create_user(self, telefone, password=None, **extra_fields):
        print("Entrei na função create_user!")  # Confirme se esta linha é chamada
        if not telefone:
            raise ValueError("O campo telefone é obrigatório")
    
        codigo_verificacao = str(random.randint(1000, 9999))
    
        # Criação do usuário
        user = self.model(telefone=telefone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
        print("Usuário criado e código de verificação gerado!")  # Verifique se o usuário foi criado
    
    # Envia o código de verificação
        print("Enviando código de verificação...")
        enviar_mensagem_wppconnect(telefone, f"Seu código de verificação é: {codigo_verificacao}")
    
        return user

    def create_superuser(self, telefone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(telefone, password, **extra_fields)




class Cliente(AbstractBaseUser):

    nome_completo = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, unique=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=200, default=make_password("hash_senha_padrao"))
    codigo_verificacao = models.CharField(max_length=5, null=True, blank=True)
    codigo_recuperacao = models.CharField(max_length=5, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ClienteManager()

    USERNAME_FIELD = "telefone"
    REQUIRED_FIELDS = ["nome_completo"]


    
    def get(self, request, *args, **kwargs):
        print("Request user:", request.user)
        return super().get(request, *args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff


    def check_password(self, password):
        return check_password(password,self.password)
    

    def __str__(self):
        return self.nome_completo