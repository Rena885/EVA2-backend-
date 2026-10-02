
from rest_framework import permissions

class IsCoordinador(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol == 'COORDINADOR'
        )
