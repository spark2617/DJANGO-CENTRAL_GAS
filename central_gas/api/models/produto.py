from django.db import models
from api.models.empresa import Empresa

class Produto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome



class PrecoProdutoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="precos")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="precos")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.empresa.nome} - {self.produto.nome} - R$ {self.preco}"

