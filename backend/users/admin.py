from datetime import date

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext as _

from hijack_admin.admin import HijackUserAdminMixin
from import_export.admin import ImportExportActionModelAdmin

from .models import User, Company
from .resources import UserResource, CompanyResource


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, HijackUserAdminMixin, DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "acronym",
        "is_staff",
        "company",
        "hijack_field",
    )
    list_display_links = ("username",)
    list_select_related = ("company",)
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "company")
    ordering = ("first_name", "last_name", "acronym")
    fieldsets = (
        (_("Información de sistema"), {"fields": ("username", "password")}),
        (_("Información personal"), {"fields": ("first_name", "last_name", "acronym", "email")}),
        (_("Información laboral"), {"fields": ("company",)}),
        (_("Permisos"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Fechas de sistema"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("last_login", "date_joined")
    resource_class = UserResource
    actions = admin.ModelAdmin.actions + ["export_admin_action", "assign_year_holidays", "assign_next_year_holidays"]

    @admin.action(description=_("Asignar vacaciones anuales (año en curso)"))
    def assign_year_holidays(self, request, queryset, year=None):
        rows_updated = queryset.count()

        for user in queryset.all():
            user.assign_year_holidays(year)

        if rows_updated == 1:
            message_bit = _("1 usuario")
        else:
            message_bit = _("{rows_updated} usuarios").format(rows_updated=rows_updated)
        self.message_user(
            request, _("Vacaciones de {message_bit} asignadas correctamente.").format(message_bit=message_bit)
        )

    @admin.action(description=_("Asignar vacaciones anuales (año que viene)"))
    def assign_next_year_holidays(self, request, queryset):
        year = date.today().year + 1
        self.assign_year_holidays(request, queryset, year)


@admin.register(Company)
class CompanyAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    fieldsets = (
        (_("Información básica"), {"fields": ("name",)}),
        (_("Vacaciones"), {"fields": ("yearly_holiday_allocation", "extra_holiday_with_green_working_days")}),
    )
    ordering = ("name",)
    resource_class = CompanyResource
