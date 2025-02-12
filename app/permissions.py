from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso de administradores.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsRegularUser(permissions.BasePermission):
    """
    Permite acesso de usuários comuns.
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_admin
