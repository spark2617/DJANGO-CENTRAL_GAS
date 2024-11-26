from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class IsAuthenticatedWithMessage(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def denied(self, request, view):
        return Response({"error": "Você não está autenticado. Faça login para acessar este recurso."}, status=401)
