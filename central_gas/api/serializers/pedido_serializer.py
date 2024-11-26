from rest_framework import serializers
from api.models.pedido import Pedido
from api.models.produto import Produto
from api.serializers.produto_serializer import ProdutoSerializer

class PedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer()
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'produto', 'data_pedido', 'expectativa', 'quantidade', 'preco', "nome_empresa"]


    def get_preco(self, obj):
        # Verifica se há preços associados ao produto e retorna o primeiro preço
        if obj.produto.precos_associados:
            return obj.produto.precos_associados[0].preco
        return None

    def create(self, validated_data):
        produto = validated_data.pop('produto_id')
        pedido = Pedido.objects.create(produto=produto, **validated_data)
        return pedido
