from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasAdminRole(BasePermission):
    """
    Права для пользователя с ролью администратора и для суперпользователя.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class HasModeratorRole(BasePermission):
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
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор или только чтение"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class AdminModeratorAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
