from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на принадлежность объекта к администратору."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """Проверка на принадлежность объекта."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
