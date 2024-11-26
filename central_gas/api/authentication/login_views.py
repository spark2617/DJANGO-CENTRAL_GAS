from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.authentication.login_serializer import LoginSerializer
from api.models.cliente import Cliente
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from api.authentication.backends import ClienteBackend

@permission_classes([AllowAny])
class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            telefone = serializer.validated_data['telefone']
            password = serializer.validated_data['password']

            try:
                user = ClienteBackend.authenticate(self,request, username= telefone, password=password)
                
            except Cliente.DoesNotExist:
                return Response({"error": "Número de telefone não registrado"}, status=status.HTTP_400_BAD_REQUEST)

            
            if not user:

                return Response({"error": "Número de telefone ou senha inválidos."}, status=status.HTTP_400_BAD_REQUEST)
            
            token, create = Token.objects.get_or_create(user=user)

            return Response({"message": "Login bem-sucedido!", "token":token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
