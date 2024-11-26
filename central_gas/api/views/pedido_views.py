from rest_framework import viewsets
from api.models.pedido import Pedido
from api.serializers.pedido_serializer import PedidoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.models.produto import Produto
from api.serializers.pedido_serializer import PedidoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.utils.localizacao import buscar_empresa_com_produtos_proximas
from api.models.produto import PrecoProdutoEmpresa
from django.db.models import Prefetch

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_queryset(self):
        cliente = self.request.user
        if cliente.is_authenticated:
            return Pedido.objects.filter(cliente=cliente).prefetch_related(
                Prefetch(
                    'produto__precos',
                    queryset=PrecoProdutoEmpresa.objects.select_related('empresa'),
                    to_attr='precos_associados'
                )
            )
        return Pedido.objects.none()



    from django.db.models import Prefetch

    def create(self, request, *args, **kwargs):
        cliente = request.user

        if not cliente.is_authenticated:
            return Response({"error": "Usuário não autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        produto_id = request.data.get("produto_id")
        expectativa = request.data.get("expectativa")
        quantidade = request.data.get("quantidade")

        if not produto_id:
            return Response({"error": "Produto é obrigatório para criar um pedido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            produto = Produto.objects.prefetch_related(
                Prefetch(
                    'precos',
                    queryset=PrecoProdutoEmpresa.objects.select_related('empresa'),
                    to_attr='precos_associados'
                )
            ).get(id=produto_id)
        except Produto.DoesNotExist:
            return Response({"error": "Produto com o ID fornecido não existe."}, status=status.HTTP_400_BAD_REQUEST)

        pedido = Pedido.objects.create(cliente=cliente, produto=produto, expectativa=expectativa, quantidade= quantidade)
        serializer = self.get_serializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BuscarEmpresasAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Permissão para usuários autenticados

    def post(self, request, *args, **kwargs):
        # Recupera o token do cliente e a lista de produtos da requisição
        token = request.auth.key
        lista_produtos = request.data.get("produtos", [])

        if not lista_produtos:
            return Response(
                {"error": "A lista de produtos é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chama a função para buscar empresas
        resultado = buscar_empresa_com_produtos_proximas(token, lista_produtos)

        if "error" in resultado:
            return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

        return Response(resultado, status=status.HTTP_200_OK)
