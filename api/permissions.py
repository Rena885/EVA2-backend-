    
from rest_framework import permissions

class IsCoordinador(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol == 'COORDINADOR'
        )


"""
RR -Permisos RBAC: Permiso personalizado. Bloquea peticiones
destructivas si no es COORDINADOR.
"""
class IsCoordinadorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol in ['COORDINADOR', 'ADMIN']
        )
