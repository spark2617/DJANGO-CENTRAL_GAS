from rest_framework import serializers
from api.models.produto import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"

    def get_preco(self, obj):
        # Lida com a ausência do atributo precos_associados
        precos_associados = getattr(obj, 'precos_associados', None)
        if precos_associados:
            # Substitua 'preco' pelo nome correto do campo
            return [preco.preco for preco in precos_associados]  # Certifique-se de que "preco" é o nome do campo correto
        return None

