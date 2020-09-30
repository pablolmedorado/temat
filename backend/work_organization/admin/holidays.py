from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin

from ..models import Holiday, HolidayType
from ..resources import HolidayResource, HolidayTypeResource


@admin.register(HolidayType)
class HolidayTypeAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "validity", "system")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = (
        (_("Información básica"), {"fields": ("name",)}),
        (_("Validez"), {"fields": ("validity",)}),
        (_("Gestión interna"), {"fields": ("system",)}),
    )
    readonly_fields = ("system",)
    resource_class = HolidayTypeResource

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.system:
            return self.readonly_fields + ("name",)
        return self.readonly_fields


@admin.register(Holiday)
class HolidayAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "user", "type", "allowance_date", "expiration_date", "planned_date", "approved")
    list_select_related = ("user", "type")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("approved", "user", "allowance_date", "planned_date")
    ordering = ("-planned_date", "-approved", "allowance_date", "user")
    fieldsets = (
        (_("Usuario"), {"fields": ("user",)}),
        (_("Clasificación"), {"fields": ("type",)}),
        (_("Disponibilidad"), {"fields": ("allowance_date", "planned_date", "approved")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
        (_("Enlaces"), {"fields": ("green_working_day",)}),
    )
    readonly_fields = (
        "creation_user",
        "creation_datetime",
        "modification_user",
        "modification_datetime",
        "green_working_day",
    )
    resource_class = HolidayResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user",)
        return self.readonly_fields
