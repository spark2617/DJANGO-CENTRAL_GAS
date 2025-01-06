from django.db import models
from .endereco import Endereco
from .user import CustomUser
from django.conf import settings


class Empresa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresa')
    nome = models.CharField(max_length=100)
    numero_licenca = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=100, null=True, blank=True)
    razao_social = models.CharField(max_length=200, null=True, blank=True)
    empresa_apresentada = models.BooleanField(default=False)
    imagem_contrato_social = models.ImageField(upload_to='contratos_sociais/', null=True, blank=True)
    logo = models.ImageField(upload_to='logo_empresas/', null=True, blank=True)
    endereco = models.OneToOneField('Endereco', on_delete=models.CASCADE, related_name="empresa", null=True, blank=True)

    def __str__(self):
        return self.nome_fantasia or self.nome
