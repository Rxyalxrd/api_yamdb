from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Пользователь с ролью администратора и для суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """Администратор или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin
                or request.user.is_superuser)
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
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user.is_superuser
                 or request.user == obj.author)
        )
