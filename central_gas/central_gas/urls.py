from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ClienteViewSet, EnderecoViewSet, EmpresaViewSet, ProdutoViewSet, PedidoViewSet
from api.authentication.login_views import LoginView
from django.contrib import admin
from api.views.cliente_views import VerificarCodigoAPIView, ReenviarCodigoAPIView, AtualizarSenhaAPIView, RecuperarSenhaAPIView, VerificarCodigoDeRecuperaçãoAPIView
from api.views.pedido_views import BuscarEmpresasAPIView


router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'enderecos', EnderecoViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'pedidos', PedidoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path("verification_code/", VerificarCodigoAPIView.as_view(), name="verify_code"),
    path("verification_code_recuperação/", VerificarCodigoDeRecuperaçãoAPIView.as_view(), name="verify_code_recuperation"),
    path("Reenviar_codigo/", ReenviarCodigoAPIView.as_view(), name="reenviar_codigo"),
    path("recuperar_senha/", RecuperarSenhaAPIView.as_view(), name="recuperar_senha"),
    path("atualizar_senha/", AtualizarSenhaAPIView.as_view(), name="definir_nova_senha"),
    path('buscar-empresa-mais-proxima/',BuscarEmpresasAPIView.as_view() , name='buscar_empresa_mais_proxima'),
    

]
