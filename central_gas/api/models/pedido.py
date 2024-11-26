from django.db import models
from .produto import Produto, PrecoProdutoEmpresa

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='pedidos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    expectativa = models.DateTimeField(null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=1)


    def nome_empresa(self):
        # Retorna o nome da empresa associada ao produto do pedido
        preco_produto = PrecoProdutoEmpresa.objects.filter(produto=self.produto).first()
        if preco_produto:
            return preco_produto.empresa.nome
        return None

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome_completo}"
    

