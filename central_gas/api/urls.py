from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ClienteViewSet, EnderecoViewSet, ProdutoViewSet, PedidoViewSet
from api.views.empresa_views import EmpresaRetrieveView
from api.authentication.login_views import LoginView
from api.views.user_views import VerificarCodigoAPIView, ReenviarCodigoAPIView, AtualizarSenhaAPIView, RecuperarSenhaAPIView, VerificarCodigoDeRecuperacaoAPIView
from api.views.pedido_views import BuscarEmpresasAPIView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'enderecos', EnderecoViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('company/', EmpresaRetrieveView.as_view(), name='company-retrieve'),
    path("verification_code/", VerificarCodigoAPIView.as_view(), name="verification-code"),
    path("recovery_verification_code/", VerificarCodigoDeRecuperacaoAPIView.as_view(), name="recovery-verification-code"),
    path("resend_code/", ReenviarCodigoAPIView.as_view(), name="resend-code"),
    path("recover_password/", RecuperarSenhaAPIView.as_view(), name="recover-password"),
    path("update_password/", AtualizarSenhaAPIView.as_view(), name="update-password"),
    path('find_nearest_company/', BuscarEmpresasAPIView.as_view(), name='find-nearest-company'),
    path('', include(router.urls)),
]
