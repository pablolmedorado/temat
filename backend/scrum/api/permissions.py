from datetime import timedelta

from django.utils import timezone

from rest_framework import permissions


class UserStoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["update", "partial_update", "validate"] or request.user.is_superuser:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user in [obj.development_user, obj.validation_user, obj.support_user]:
            return bool(
                request.method in permissions.SAFE_METHODS or view.action in ["update", "partial_update", "validate"]
            )
        return request.method in permissions.SAFE_METHODS


class TaskPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "toggle" or request.user.is_superuser:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user == obj.user_story.development_user:
            return bool(request.method in permissions.SAFE_METHODS or view.action == "toggle")
        return request.method in permissions.SAFE_METHODS


class EffortPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user == obj.user and obj.creation_datetime >= timezone.now() - timedelta(minutes=30):
            return True
        return request.method in permissions.SAFE_METHODS
