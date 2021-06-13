from datetime import timedelta

from django.utils import timezone

from rest_framework import permissions

from common.api.utils import check_api_user_permissions


class UserStoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["update", "partial_update", "validate"] or check_api_user_permissions(view):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if check_api_user_permissions(view):
            return True
        if request.user in [obj.development_user, obj.validation_user, obj.support_user]:
            return bool(
                request.method in permissions.SAFE_METHODS or view.action in ["update", "partial_update", "validate"]
            )
        return request.method in permissions.SAFE_METHODS


class TaskPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "toggle" or check_api_user_permissions(view):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if check_api_user_permissions(view):
            return True
        if request.user == obj.user_story.development_user:
            return bool(request.method in permissions.SAFE_METHODS or view.action == "toggle")
        return request.method in permissions.SAFE_METHODS


class EffortPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if check_api_user_permissions(view):
            return True
        if request.user == obj.user and obj.creation_datetime >= timezone.now() - timedelta(minutes=30):
            return True
        return request.method in permissions.SAFE_METHODS
