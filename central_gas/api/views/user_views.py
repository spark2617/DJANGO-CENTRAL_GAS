from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import CustomUser 
from rest_framework.permissions import AllowAny
from api.service.enviar_mensagem_whatsapp import enviar_mensagem_wppconnect
import random

class VerificarCodigoAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telefone = request.data.get('telefone')
        codigo_informado = request.data.get('codigo')

        # Verificação de campos obrigatórios
        if not telefone or not codigo_informado:
            return Response(
                {"message": "Telefone e código são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Buscar o usuário com o telefone fornecido
            user = CustomUser.objects.get(telefone=telefone)
            
            # Verificar se o código informado é igual ao código do usuário
            if user.codigo_verificacao == codigo_informado:
                # Código correto, ativa o usuário
                user.is_active = True
                user.codigo_verificacao=""
                user.save()
                return Response({"message": "Código verificado com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Código incorreto."}, status=status.HTTP_400_BAD_REQUEST)
        
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário com este telefone não encontrado."},
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
            # Buscar o usuário no modelo CustomUser (Cliente ou Empresa)
            user = CustomUser.objects.get(telefone=telefone)

            # Gerar um novo código de verificação
            novo_codigo_verificacao = str(random.randint(10000, 99999))
            user.codigo_verificacao = novo_codigo_verificacao
            user.save()

            # Enviar o código de verificação por WhatsApp (ou outro meio de comunicação)
            try:
                # Função que envia a mensagem (a lógica da função `enviar_mensagem_wppconnect` permanece)
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

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário com este telefone não encontrado."},
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
            # Verifica se o usuário existe
            user = CustomUser.objects.get(telefone=telefone)

            # Gerar código de recuperação
            codigo_recuperacao = str(random.randint(10000, 99999))
            user.codigo_recuperacao = codigo_recuperacao
            user.save()

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

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário com este telefone não encontrado."},
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
            user = CustomUser.objects.get(telefone=telefone)

            if user.codigo_recuperacao == codigo_informado:
                user.set_password(nova_senha)  # Usando set_password para criptografar a senha
                user.codigo_recuperacao = None  # Limpa o código de recuperação após a atualização
                user.save()

                return Response(
                    {"message": "Senha atualizada com sucesso."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Código incorreto."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao atualizar a senha.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class VerificarCodigoDeRecuperacaoAPIView(APIView):
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
            user = CustomUser.objects.get(telefone=telefone)
            if user.codigo_recuperacao == codigo_informado:
                # Código correto, ativa o usuário ou realiza qualquer outra alteração necessária
                user.is_active = True  # Exemplo: ativando o usuário
                user.save()
                return Response({"message": "Código verificado com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Código incorreto."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Usuário com este telefone não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro inesperado ao verificar o código.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
