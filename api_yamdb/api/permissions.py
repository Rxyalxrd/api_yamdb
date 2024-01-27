from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор или только чтение"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.is_staff or request.user.is_superuser)
        return False
