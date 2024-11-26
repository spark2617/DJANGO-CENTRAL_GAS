from rest_framework import viewsets
from api.models.empresa import Empresa
from api.serializers.empresa_serializer import EmpresaSerializer
from django.http import JsonResponse


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


