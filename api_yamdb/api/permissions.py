from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Права для пользователя с ролью администратора и для суперпользователя.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsModerator(BasePermission):
    """Права для пользователя с ролью модератора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'moderator'
        )


class IsAuthorOrReadOnly(BasePermission):
    """
    Права на редактирование и удаление собственных публикаций/комменатриев.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Администратор или только чтение"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_authenticated and request.user.role == 'admin'

# class IsAdminOrReadOnly(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return request.method in SAFE_METHODS or request.user.is_authenticated and request.user.role == 'admin'

class AdminModeratorAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
