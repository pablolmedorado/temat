from rest_framework import permissions

from .utils import check_api_user_permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    The requester is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or request.user.is_superuser)


class HasDjangoPermissionOrReadOnly(permissions.BasePermission):
    """
    The requester has the needed permission over the Django Model, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or check_api_user_permissions(view))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    The requester is the owner of the record, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or check_api_user_permissions(view):
            return True
        if not hasattr(obj, "OWNERSHIP_FIELD"):
            return False
        owner = getattr(obj, getattr(obj, "OWNERSHIP_FIELD"))
        return owner == request.user


class NotificationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or check_api_user_permissions(view):
            return True
        return obj.recipient == request.user
