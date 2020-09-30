from django.contrib.auth.models import Group

from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import viewsets

from .models import User
from .serializers import GroupSerializer, UserSerializer


class UserApi(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related("company").prefetch_related("groups").filter(is_active=True)
    serializer_class = UserSerializer
    permit_list_expands = ["company", "groups"]
    search_fields = ("username", "first_name", "last_name", "acronym")
    ordering_fields = ("id", "username", "first_name", "last_name", "acronym")
    ordering = ("acronym",)


class GroupApi(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)
