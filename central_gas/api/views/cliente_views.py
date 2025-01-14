from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from api.models.cliente import Cliente
from api.models.endereco import Endereco
from api.serializers.cliente_serializer import ClienteSerializer
from api.service.enviar_mensagem_whatsapp import enviar_mensagem_wppconnect
from django.db import IntegrityError
import random
from django.core.exceptions import ValidationError
from api.models import Cliente, Endereco, CustomUser


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_queryset(self):
        user = self.request.user
        return Cliente.objects.filter(user__telefone=user.telefone)

    def create(self, request, *args, **kwargs):
        # Dados recebidos no request
        telefone = request.data.get('telefone')
        nome_completo = request.data.get('nome_completo')
        password = request.data.get('password')
        endereco_data = request.data.get('endereco')

        # Validação de campos obrigatórios
        if not telefone or not nome_completo or not password or not endereco_data:
            return Response(
                {"message": "Campos obrigatórios não preenchidos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar se o usuário já existe
        user = CustomUser.objects.filter(telefone=telefone)
        if user.exists():
            return Response(
                {"message": "Usuário com este telefone já existe."},
                status=status.HTTP_409_CONFLICT
            )

        # Criar endereço
        try:
            endereco = Endereco.objects.create(**endereco_data)
        except ValidationError as e:
            return Response(
                {"message": "Erro ao criar endereço. Verifique os dados fornecidos.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao criar endereço.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Gerar código de verificação
        codigo_verificacao = str(random.randint(10000, 99999))

        # Criar CustomUser e Cliente
        try:
            # Criar usuário no CustomUser
            user = CustomUser.objects.create_user(
                telefone=telefone,
                password=password,
                tipo='cliente',
                codigo_verificacao=codigo_verificacao
            )
            # Criar Cliente associado ao CustomUser
            cliente = Cliente.objects.create(
                nome_completo=nome_completo,
                endereco=endereco,
                user=user
            )
        except IntegrityError as e:
            endereco.delete()  # Remove o endereço criado se o cliente ou usuário falhar
            return Response(
                {"message": "Erro ao criar o cliente. Verifique os dados fornecidos.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            endereco.delete()
            return Response(
                {"message": "Erro inesperado ao criar cliente ou usuário.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Enviar código de verificação por WhatsApp
        try:
            enviar_mensagem_wppconnect(telefone, f"Seu código de verificação é: {codigo_verificacao}")
        except Exception as e:
            error_message = str(e).lower()
            user.delete()
            endereco.delete()
            cliente.delete()
            if "sessão fechada" in error_message:
                return Response(
                    {"message": "Erro ao enviar mensagem. Sessão encerrada. Tente novamente mais tarde."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif f"número {telefone} não existe" in error_message:
                return Response(
                    {"message": "Número de telefone inválido. Verifique e tente novamente."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"message": "Erro ao enviar mensagem de verificação. Tente novamente mais tarde."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Serializar e retornar os dados do cliente criado
        serializer = self.get_serializer(cliente)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        # Permitir acesso público para criação de clientes (POST)
        if self.request.method == 'POST':
            return [AllowAny()]
        # Requer autenticação para outras ações
        return [IsAuthenticated()]


