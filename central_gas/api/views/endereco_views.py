from rest_framework import viewsets
from api.models.endereco import Endereco
from api.serializers.endereco_serializer import EnderecoSerializer

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer