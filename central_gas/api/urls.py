from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, EnderecoViewSet
from django.contrib import admin
from views.cliente_views import VerificarCodigoAPIView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'enderecos', EnderecoViewSet)

urlpatterns = [
    path('', include('api.urls')), 
]
