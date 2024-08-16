from rest_framework.permissions import BasePermission


class RequestIsAllowed(BasePermission):
    def has_permission(self, request, view):

        if request.user.groups.filter(name='Administrador').exists():
            return True
        
        if request.user.groups.filter(name='Edicion').exists():
            if request.method in ['GET', 'PUT', 'POST']:
                return True
            return False
        
        if request.user.groups.filter(name='Consulta').exists():
            if request.method in ['GET']:
                return True
            return False
        
        return False
