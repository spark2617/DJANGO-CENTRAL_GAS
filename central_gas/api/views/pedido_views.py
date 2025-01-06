from rest_framework import viewsets
from api.models.pedido import Pedido
from django.db.models import Prefetch
from api.models.cliente import Cliente
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
from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from api.service.enviar_mensagem_whatsapp import enviar_mensagem_wppconnect


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_queryset(self):
        cliente = self.request.user
        
        if cliente.is_authenticated:
            return Pedido.objects.filter(cliente__user=cliente).prefetch_related(
                Prefetch(
                    'produto__precos',  # 'produto' deve ser o nome do campo no Pedido que referencia o Produto
                    queryset=PrecoProdutoEmpresa.objects.select_related('empresa'),
                    to_attr='precos_associados'  # Isso cria um atributo 'precos_associados' no Produto
                )
            )
        return Pedido.objects.none()





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

        pedido = Pedido.objects.create(cliente=cliente.cliente, produto=produto, expectativa=expectativa, quantidade= quantidade)
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
    



def NotificarUsuarioSobreExpectativa():
    """
    Tarefa que verifica os pedidos e notifica os clientes cujas expectativas estão próximas de vencer
    através do WhatsApp.
    """
    hoje = now()
    tres_dias = hoje + timedelta(days=3)
    dois_dias = hoje + timedelta(days=2)

    # Pedidos de gás (ID do produto = 1, notificação 3 dias antes)
    pedidos_gas = Pedido.objects.filter(
        produto_id=1,  # ID do produto 'gás'
        expectativa__date=tres_dias.date()
    )

    # Pedidos de outros produtos (notificação 2 dias antes)
    pedidos_outros = Pedido.objects.filter(
        produto_id__ne=1,  # Outros produtos que não sejam gás
        expectativa__date=dois_dias.date()
    )

    # Combine os pedidos encontrados
    pedidos = list(pedidos_gas) + list(pedidos_outros)

    for pedido in pedidos:
        cliente = pedido.cliente
        produto = pedido.produto.nome
        numero_destino = cliente.user.telefone 
        mensagem = (
            f"Olá {cliente.nome}, "
            f"lembrete: seu pedido do produto '{produto}' está previsto para {pedido.expectativa}. "
            "Prepare-se com antecedência!"
        )

        # Enviar mensagem via WhatsApp
        if numero_destino:
            resultado = enviar_mensagem_wppconnect(numero_destino, mensagem)
            if "error" in resultado:
                # Log de erro ou tentativa de reenvio, se necessário
                print(f"Erro ao enviar mensagem para {numero_destino}: {resultado}")
            else:
                print(f"Mensagem enviada com sucesso para {numero_destino}")
        else:
            print(f"Cliente {cliente.nome} não possui número de telefone cadastrado.")
        