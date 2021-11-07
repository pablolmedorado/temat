from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django_currentuser.middleware import get_current_authenticated_user
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Event, EventType
from common.widgets import UUIDWidget


class EventResource(resources.ModelResource):
    type = Field(attribute="type", widget=ForeignKeyWidget(model=EventType, field="name"), readonly=False)
    attendees = Field(
        attribute="attendees", widget=ManyToManyWidget(model=get_user_model(), field="username"), readonly=False
    )
    groups = Field(attribute="groups", widget=ManyToManyWidget(model=Group, field="name"), readonly=False)
    creation_user = Field(
        attribute="creation_user",
        widget=ForeignKeyWidget(model=get_user_model(), field="username"),
        readonly=False,
        default=get_current_authenticated_user,
    )
    link_object_id = Field(attribute="link_object_id", widget=UUIDWidget(), readonly=False)

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
            "creation_user",
        )
        export_order = fields


class EventTypeResource(resources.ModelResource):
    class Meta:
        model = EventType
        fields = ("id", "name", "colour", "icon", "important", "system_slug")
        export_order = fields
