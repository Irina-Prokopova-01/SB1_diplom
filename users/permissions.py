from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на принадлежность объекта к администратору."""

    def has_permission(self, request, view):
        return (
                request.user.role == "admin" or request.method
                in permissions.SAFE_METHODS)


class IsOwner(permissions.BasePermission):
    """Проверка на принадлежность объекта."""

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.method
                in permissions.SAFE_METHODS)
