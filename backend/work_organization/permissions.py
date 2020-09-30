from rest_framework import permissions


class HolidayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["request", "cancel"] or request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user == obj.user:
            return bool(request.method in permissions.SAFE_METHODS or view.action == "cancel")
        return request.method in permissions.SAFE_METHODS


class GreenWorkingDayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "toggle_volunteer" or request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return bool(request.method in permissions.SAFE_METHODS or view.action == "toggle_volunteer")
