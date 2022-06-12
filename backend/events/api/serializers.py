from colorfield.serializers import ColorField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from django.utils.translation import ugettext_lazy as _

from common.api.serializers import TagSerializer
from users.api.serializers import GroupSerializer, UserSerializer
from ..models import Event, EventType


class EventTypeSerializer(FlexFieldsModelSerializer):
    colour = ColorField(required=False)

    class Meta:
        model = EventType
        fields = ("id", "name", "colour", "icon", "important", "system_slug")
        read_only_fields = ("id", "system_slug")


class EventSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    tags = TagListSerializerField()

    def validate_type(self, value):
        if value.system_slug:
            raise serializers.ValidationError(_("No es posible crear un evento con un tipo reservado al sistema"))
        return value

    def validate(self, data):
        data = super().validate(data)
        if data.get("end_datetime") < data.get("start_datetime"):
            raise serializers.ValidationError(
                _("No es posible crear un evento con fecha de fin anterior a la de inicio")
            )
        return data

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "type",
            "details",
            "start_datetime",
            "end_datetime",
            "all_day",
            "visibility",
            "location",
            "attendees",
            "groups",
            "tags",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        read_only_fields = (
            "id",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        expandable_fields = {
            "type": EventTypeSerializer,
            "attendees": (UserSerializer, {"many": True}),
            "groups": (GroupSerializer, {"many": True}),
            "tags": (TagSerializer, {"many": True, "fields": ["name", "colour", "icon"]}),
        }
