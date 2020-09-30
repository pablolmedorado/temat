from django.utils.translation import ugettext_lazy as _

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from users.serializers import GroupSerializer, UserSerializer

from .models import Event, EventType


class EventTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = EventType
        fields = ("id", "name", "colour", "icon", "important", "system")
        read_only_fields = ("id", "system")


class EventSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    tags = TagListSerializerField()

    def validate(self, data):
        data = super().validate(data)
        if data.get("end_datetime") < data.get("start_datetime"):
            raise serializers.ValidationError(
                _("No es posible crear un evento con fecha de fin anterior a la de inicio")
            )
        if data.get("type").system:
            raise serializers.ValidationError(_("No es posible crear un evento con un tipo reservado al sistema"))
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
        }
