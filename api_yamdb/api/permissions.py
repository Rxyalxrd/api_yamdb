from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Пользователь с ролью администратора и для суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """Администратор или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
        )


class AdminModeratorAuthorOrReadOnly(BasePermission):
    """Редактирование админом, модератором или автором."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
