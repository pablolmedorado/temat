from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..decorators import atomic_transaction_singleton
from ..models import Link, Tag
from .filtersets import NotificationFilterSet, TagFilterSet
from .mixins import AtomicBulkDestroyModelMixin
from .permissions import NotificationPermission
from .serializers import LinkSerializer, NotificationSerializer, TagSerializer


class NotificationViewSet(
    FlexFieldsMixin,
    mixins.RetrieveModelMixin,
    AtomicBulkDestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticated, NotificationPermission)
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilterSet
    search_fields = ("verb", "description")
    ordering_fields = ("id", "level", "unread", "timestamp", "target_content_type__model")
    ordering = ("-unread", "-timestamp")

    def get_queryset(self, *args, **kwargs):
        return self.request.user.notifications.select_related("actor_content_type", "target_content_type")

    @action(detail=False, methods=["GET"])
    def unread_count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().unread())
        return Response({"count": queryset.count()})

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def mark_as_read(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @atomic_transaction_singleton
    @action(detail=False, methods=["PATCH"])
    def mark_all_as_read(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.mark_all_as_read()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def mark_as_unread(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.mark_as_unread()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @atomic_transaction_singleton
    @action(detail=False, methods=["PATCH"])
    def mark_all_as_unread(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.mark_all_as_unread()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_class = TagFilterSet
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class LinkViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permit_list_expands = ["type"]
    search_fields = ("name", "url")
    ordering_fields = ()
