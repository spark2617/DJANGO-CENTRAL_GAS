from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.expo_push_token import ExpoPushToken

class SaveExpoTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        user = request.user
        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Salvar ou atualizar o token
        ExpoPushToken.objects.update_or_create(user=user, defaults={'token': token})
        return Response({"message": "Token saved successfully"}, status=status.HTTP_200_OK)
