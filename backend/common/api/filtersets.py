from django_filters.rest_framework import FilterSet

from notifications.models import Notification

from ..models import Tag


class NotificationFilterSet(FilterSet):
    class Meta:
        model = Notification
        fields = {
            "id": ["exact", "in"],
            "level": ["exact", "in"],
            "recipient": ["exact", "in"],
            "unread": ["exact"],
            "actor_content_type": ["exact", "in"],
            "actor_object_id": ["exact", "in"],
            "verb": ["icontains"],
            "description": ["icontains"],
            "target_content_type": ["exact", "in"],
            "target_content_type__model": ["exact", "in"],
            "target_object_id": ["exact", "in"],
            "timestamp": ["exact", "gte", "lte", "date", "date__lte", "date__gte"],
        }


class TagFilterSet(FilterSet):
    class Meta:
        model = Tag
        fields = {
            "id": ["exact", "in"],
            "name": ["in", "iexact", "icontains", "istartswith"],
            "slug": ["in", "exact"],
        }
