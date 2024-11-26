from api.models.produto import Produto
from api.serializers.produto_serializer import ProdutoSerializer
from rest_framework import viewsets

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer