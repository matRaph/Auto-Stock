from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso de administradores.
    """

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Administrador").exists()


class IsRegularUser(permissions.BasePermission):
    """
    Permite acesso de usuários comuns.
    """

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Comum").exists()
