from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin

from .models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay
from .resources import GreenWorkingDayResource, HolidayResource, HolidayTypeResource, SupportWorkingDayResource


@admin.register(GreenWorkingDay)
class GreenWorkingDayAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "date", "label")
    list_display_links = ("date",)
    search_fields = ("label",)
    list_filter = ("users", "date")
    ordering = ("-date",)
    fieldsets = (
        (_("Información básica"), {"fields": ("date", "label")}),
        (_("Usuarios"), {"fields": ("users", "volunteers")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    filter_horizontal = (
        "users",
        "volunteers",
    )
    readonly_fields = ("creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = GreenWorkingDayResource


@admin.register(SupportWorkingDay)
class SupportWorkingDayAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "user", "date")
    list_select_related = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("user", "date")
    ordering = ("-date",)
    fieldsets = (
        (_("Usuario"), {"fields": ("user",)}),
        (_("Fecha"), {"fields": ("date",)}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    readonly_fields = ("creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = SupportWorkingDayResource


@admin.register(HolidayType)
class HolidayTypeAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "validity", "system_slug")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = (
        (_("Información básica"), {"fields": ("name",)}),
        (_("Validez"), {"fields": ("validity",)}),
        (_("Gestión interna"), {"fields": ("system_slug",)}),
    )
    readonly_fields = ("system_slug",)
    resource_class = HolidayTypeResource

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.system_slug:
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
