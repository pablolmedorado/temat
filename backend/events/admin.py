from django.contrib import admin
from django.utils.translation import ugettext as _

from import_export.admin import ImportExportActionModelAdmin

from .models import Event, EventType
from .resources import EventTypeResource, EventResource


@admin.register(EventType)
class EventTypeAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "icon", "colored_colour", "important", "system_slug")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("important",)
    ordering = ("name",)
    fieldsets = (
        (_("Información básica"), {"fields": ("name", "important")}),
        (_("Apariencia"), {"fields": ("colour", "icon")}),
        (_("Gestión interna"), {"fields": ("system_slug",)}),
    )
    readonly_fields = ("system_slug",)
    resource_class = EventTypeResource

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.system_slug:
            return self.readonly_fields + ("name",)
        return self.readonly_fields


@admin.register(Event)
class EventAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "type", "start_datetime", "end_datetime", "all_day", "visibility", "creation_user")
    list_select_related = ("type", "creation_user")
    search_fields = ("name", "details", "location")
    list_filter = ("type", "visibility", "attendees", "groups")
    ordering = ("-start_datetime", "-all_day")
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("name", "details")}),
        (_("Clasificación"), {"fields": ("type", "tags")}),
        (_("Información temporal"), {"fields": ("start_datetime", "end_datetime", "all_day")}),
        (_("Localización"), {"fields": ("location",)}),
        (_("Visibilidad"), {"fields": ("visibility",)}),
        (_("Invitados"), {"fields": ("attendees", "groups")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
        (_("Enlace"), {"fields": ("link_content_type", "link_object_id")}),
    )
    filter_horizontal = ("attendees", "groups")
    readonly_fields = (
        "id",
        "creation_user",
        "creation_datetime",
        "modification_user",
        "modification_datetime",
        "link_content_type",
        "link_object_id",
    )
    resource_class = EventResource
