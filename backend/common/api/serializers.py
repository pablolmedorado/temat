from notifications.models import Notification
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from taggit.models import Tag

from ..models import Link, LinkType
from users.api.serializers import UserSerializer


class NotificationTargetSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    representation = serializers.CharField(source="notification_str", read_only=True)


class NotificationSerializer(FlexFieldsModelSerializer):
    actor = UserSerializer(fields=["id", "username", "acronym", "first_name", "last_name"], read_only=True)
    target_content_type = serializers.SlugRelatedField(slug_field="model", read_only=True)
    target = NotificationTargetSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "level",
            "unread",
            "recipient",
            "timestamp",
            "timesince",
            "actor",
            "verb",
            "target_content_type",
            "target",
            "description",
        )
        read_only_fields = fields


class TagSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = fields


class LinkTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = LinkType
        fields = ("id", "name", "order")
        read_only_fields = fields


class LinkSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Link
        fields = ("id", "name", "icon", "url", "type", "order")
        read_only_fields = fields
        expandable_fields = {
            "type": LinkTypeSerializer,
        }
