from django.contrib.auth.models import Group

from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import viewsets

from .serializers import GroupSerializer, UserSerializer
from ..models import User


class UserViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related("company").prefetch_related("groups")
    serializer_class = UserSerializer
    permit_list_expands = ["company", "groups"]
    filterset_fields = ("is_active",)
    search_fields = ("username", "first_name", "last_name", "acronym")
    ordering_fields = ("id", "username", "first_name", "last_name", "acronym")
    ordering = ("acronym",)


class GroupViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)
