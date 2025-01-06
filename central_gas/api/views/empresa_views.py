from rest_framework import generics
from api.models import Empresa
from api.serializers.empresa_serializer import EmpresaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class EmpresaRetrieveView(generics.RetrieveAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
       
        user = self.request.user
        
        
        try:
            return user.empresa
        except Empresa.DoesNotExist:
            raise Response(detail="Empresa não encontrada para este usuário.")
