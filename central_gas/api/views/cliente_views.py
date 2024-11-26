from rest_framework import viewsets, status
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


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_queryset(self):
        user = self.request.user
        return Cliente.objects.filter(telefone=user.telefone)


    def create(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')
        nome_completo = request.data.get('nome_completo')
        password = request.data.get('password')
        endereco_data = request.data.get("endereco")

        if not telefone or not nome_completo or not password or not endereco_data:
            return Response(
                {"message": "Campos obrigatórios não preenchidos."},
                status=status.HTTP_400_BAD_REQUEST
            )
        cliente = Cliente.objects.filter(telefone=telefone)
        # Verificação de usuário existente
        if cliente.exists() and cliente.first().is_active:
            return Response(
                {"message": "Usuário com este telefone já existe."},
                status=status.HTTP_409_CONFLICT
            )
        if cliente.exists() and not cliente.first().is_active:
            cliente.first().delete()

        try:
            # Criação do endereço associado
            endereco = Endereco.objects.create(**endereco_data)
        except ValidationError as e:
            return Response(
                {"message": "Erro ao criar usuário. Verifique os dados de endereço fornecidos.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Ocorreu um erro inesperado ao criar o endereço.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Gerar código de verificação
        codigo_verificacao = str(random.randint(10000, 99999))

        try:
            # Criação do usuário com o código de verificação
            user = Cliente.objects.create(
                telefone=telefone,
                nome_completo=nome_completo,
                password=password,
                codigo_verificacao=codigo_verificacao,
                endereco=endereco
            )
        except IntegrityError as e:
            endereco.delete()  # Remove o endereço criado se o cliente não for criado
            return Response(
                {"message": "Erro ao criar o usuário. Verifique os dados fornecidos.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            endereco.delete()
            return Response(
                {"message": "Ocorreu um erro inesperado ao criar o usuário.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Enviar código de verificação por WhatsApp
        try:
            enviar_mensagem_wppconnect(telefone, f"Seu código de verificação é: {codigo_verificacao}")
            
        except Exception as e:
            # Checa o tipo de erro
            error_message = str(e)
            if "sessão fechada" in error_message.lower():
                # Deleta usuário e endereço, pois houve um problema de sessão no envio
                user.delete()
                endereco.delete()
                return Response(
                    {"message": "Erro ao enviar a mensagem de verificação. A sessão foi encerrada. Tente novamente mais tarde.", "error": error_message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif f"número {telefone} não existe" in error_message.lower():
                # Deleta usuário e endereço, pois o número não é válido
                user.delete()
                endereco.delete()
                return Response(
                    {"message": "Erro ao enviar a mensagem de verificação. Número de telefone inválido.", "error": error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Outros erros inesperados
                user.delete()
                endereco.delete()
                return Response(
                    {"message": "Erro ao enviar a mensagem de verificação. Tente novamente mais tarde.", "error": error_message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Serializa o objeto e retorna a resposta
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


class VerificarCodigoAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')
        codigo_informado = request.data.get('codigo')

        if not telefone or not codigo_informado:
            return Response(
                {"message": "Telefone e código são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cliente = Cliente.objects.get(telefone=telefone)
            if cliente.codigo_verificacao == codigo_informado:
                # Código correto, ativa o usuário
                cliente.is_active = True  # Ativa o usuário ou faz qualquer outra alteração necessária
                cliente.save()
                return Response({"message": "Código verificado com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Código incorreto."}, status=status.HTTP_400_BAD_REQUEST)
        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao verificar o código.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReenviarCodigoAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')

        if not telefone:
            return Response(
                {"message": "Telefone é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cliente = Cliente.objects.get(telefone=telefone)

            
            novo_codigo_verificacao = str(random.randint(10000, 99999))
            cliente.codigo_verificacao = novo_codigo_verificacao
            cliente.save()

            
            try:
                enviar_mensagem_wppconnect(telefone, f"Seu novo código de verificação é: {novo_codigo_verificacao}")
                return Response(
                    {"message": "Código de verificação reenviado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                error_message = str(e)
                if "sessão fechada" in error_message.lower():
                    return Response(
                        {"message": "Erro ao enviar a mensagem de verificação. A sessão foi encerrada. Tente novamente mais tarde.", "error": error_message},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                elif f"número {telefone} não existe" in error_message.lower():
                    return Response(
                        {"message": "Erro ao enviar a mensagem de verificação. Número de telefone inválido.", "error": error_message},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"message": "Erro ao enviar a mensagem de verificação. Tente novamente mais tarde.", "error": error_message},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao reenviar o código de verificação.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class RecuperarSenhaAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')

        if not telefone:
            return Response(
                {"message": "Telefone é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verifica se o cliente existe
            cliente = Cliente.objects.get(telefone=telefone)

            # Gerar código de recuperação
            codigo_recuperacao = str(random.randint(10000, 99999))
            cliente.codigo_recuperacao = codigo_recuperacao 
            cliente.save()

            # Enviar código de recuperação por WhatsApp
            try:
                enviar_mensagem_wppconnect(telefone, f"Seu código de recuperação de senha é: {codigo_recuperacao}")
                return Response(
                    {"message": "Código de recuperação enviado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                error_message = str(e)
                if "sessão fechada" in error_message.lower():
                    return Response(
                        {"message": "Erro ao enviar a mensagem. A sessão foi encerrada. Tente novamente mais tarde.", "error": error_message},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                elif f"número {telefone} não existe" in error_message.lower():
                    return Response(
                        {"message": "Erro ao enviar a mensagem. Número de telefone inválido.", "error": error_message},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"message": "Erro ao enviar a mensagem. Tente novamente mais tarde.", "error": error_message},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao solicitar a recuperação de senha.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AtualizarSenhaAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')
        codigo_informado = request.data.get('codigo')
        nova_senha = request.data.get('nova_senha')

        if not telefone or not codigo_informado or not nova_senha:
            return Response(
                {"message": "Telefone, código e nova senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            
            cliente = Cliente.objects.get(telefone=telefone)

            
            if cliente.codigo_recuperacao == codigo_informado:
                
                cliente.password = nova_senha  
                cliente.codigo_recuperacao = None
                cliente.save()

                return Response(
                    {"message": "Senha atualizada com sucesso."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Código incorreto."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao atualizar a senha.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerificarCodigoDeRecuperaçãoAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')
        codigo_informado = request.data.get('codigo')

        if not telefone or not codigo_informado:
            return Response(
                {"message": "Telefone e código são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cliente = Cliente.objects.get(telefone=telefone)
            if cliente.codigo_recuperacao == codigo_informado:
                # Código correto, ativa o usuário
                cliente.is_active = True  # Ativa o usuário ou faz qualquer outra alteração necessária
                cliente.save()
                return Response({"message": "Código verificado com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Código incorreto."}, status=status.HTTP_400_BAD_REQUEST)
        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao verificar o código.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )