from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from api.authentication.login_serialazer import LoginSerializer
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Gere ou recupere o token associado ao usuário
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'tipo': user.tipo,
        }, status=status.HTTP_200_OK)
