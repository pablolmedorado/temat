from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Event, EventType


class EventResource(resources.ModelResource):
    type = Field(attribute="type", widget=ForeignKeyWidget(model=EventType, field="name"), readonly=False)
    attendees = Field(
        attribute="attendees", widget=ManyToManyWidget(model=get_user_model(), field="username"), readonly=False
    )
    groups = Field(attribute="groups", widget=ManyToManyWidget(model=Group, field="name"), readonly=False)

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
            "link_content_type",
            "link_object_id",
        )
        export_order = fields


class EventTypeResource(resources.ModelResource):
    class Meta:
        model = EventType
        fields = ("id", "name", "colour", "icon", "important", "system")
        export_order = fields
