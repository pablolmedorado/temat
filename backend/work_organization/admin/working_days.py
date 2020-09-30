from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin

from ..models import GreenWorkingDay, SupportWorkingDay
from ..resources import GreenWorkingDayResource, SupportWorkingDayResource


@admin.register(GreenWorkingDay)
class GreenWorkingDayAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "date", "label", "main_user", "support_user")
    list_display_links = ("date",)
    list_select_related = ("main_user", "support_user")
    search_fields = (
        "label",
        "main_user__username",
        "main_user__first_name",
        "main_user__last_name",
        "support_user__username",
        "support_user__first_name",
        "support_user__last_name",
    )
    list_filter = ("main_user", "support_user", "date")
    ordering = ("-date",)
    fieldsets = (
        (_("Información básica"), {"fields": ("date", "label")}),
        (_("Usuarios"), {"fields": ("main_user", "support_user", "volunteers")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    filter_horizontal = ("volunteers",)
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
