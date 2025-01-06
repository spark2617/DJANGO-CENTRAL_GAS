from django.db import models
from .endereco import Endereco
from .user import CustomUser

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cliente')
    nome_completo = models.CharField(max_length=200)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome_completo
