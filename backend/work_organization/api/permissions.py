from rest_framework import permissions

from common.api.utils import check_api_user_permissions


class HolidayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["request", "cancel"] or check_api_user_permissions(view):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if check_api_user_permissions(view):
            return True
        if request.user == obj.user:
            return bool(request.method in permissions.SAFE_METHODS or view.action == "cancel")
        return request.method in permissions.SAFE_METHODS


class GreenWorkingDayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "toggle_volunteer" or check_api_user_permissions(view):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if check_api_user_permissions(view):
            return True
        return bool(request.method in permissions.SAFE_METHODS or view.action == "toggle_volunteer")
