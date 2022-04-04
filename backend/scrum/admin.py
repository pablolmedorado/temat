from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin

from .models import (
    Effort,
    Epic,
    Progress,
    Sprint,
    Task,
    UserStory,
    UserStoryType,
)
from .resources import (
    EffortResource,
    EpicResource,
    ProgressResource,
    SprintResource,
    TaskResource,
    UserStoryResource,
    UserStoryTypeResource,
)


@admin.register(Sprint)
class SprintAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "start_date", "end_date", "accountable_user")
    list_select_related = ("accountable_user",)
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("accountable_user", "start_date", "end_date")
    ordering = ("-start_date",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("name",)}),
        (_("Información temporal"), {"fields": ("start_date", "end_date")}),
        (_("Actores"), {"fields": ("accountable_user",)}),
        (_("Clasificación"), {"fields": ("tags",)}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    readonly_fields = ("id", "creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = SprintResource


@admin.register(Epic)
class EpicAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name", "description")
    ordering = ("name",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("name",)}),
        (_("Descripción"), {"fields": ("description",)}),
        (_("Enlaces"), {"fields": ("external_reference",)}),
        (_("Clasificación"), {"fields": ("tags",)}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    readonly_fields = ("id", "creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = EpicResource


@admin.register(UserStoryType)
class UserStoryTypeAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "colored_colour")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = (
        (_("Información básica"), {"fields": ("name",)}),
        (_("Apariencia"), {"fields": ("colour",)}),
    )
    resource_class = UserStoryTypeResource


class TaskInLine(admin.TabularInline):
    model = Task
    fields = ("name", "weight", "done")
    raw_id_fields = ("user_story",)
    extra = 1


@admin.register(UserStory)
class UserStoryAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "epic", "type", "planned_effort", "sprint", "status")
    list_select_related = ("epic", "type", "sprint")
    search_fields = ("name", "functional_description", "technical_description")
    list_filter = ("type", "status")
    ordering = ("-start_date",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("name",)}),
        (_("Clasificación"), {"fields": ("epic", "type", "tags")}),
        (
            _("Descripción"),
            {"fields": ("functional_description", "technical_description", "priority", "planned_effort")},
        ),
        (_("Información temporal"), {"fields": ("sprint", "start_date", "end_date")}),
        (
            _("Estado"),
            {
                "fields": (
                    "current_progress",
                    "current_progress_changed",
                    "validated",
                    "validated_changed",
                    "status",
                    "risk_level",
                    "risk_comments",
                )
            },
        ),
        (
            _("Actores"),
            {
                "fields": (
                    "development_user",
                    "development_comments",
                    "validation_user",
                    "validation_comments",
                    "support_user",
                    "support_comments",
                )
            },
        ),
        (_("SCV"), {"fields": ("cvs_branch_name", "cvs_issue_id", "cvs_pull_request_id")}),
        (_("Despliegue"), {"fields": ("use_migrations", "deployment_notes")}),
        (_("Miscelánea"), {"fields": ("external_resource",)}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    raw_id_fields = ("epic", "sprint")
    readonly_fields = (
        "id",
        "creation_user",
        "creation_datetime",
        "modification_user",
        "modification_datetime",
        "current_progress",
        "current_progress_changed",
        "validated_changed",
        "status",
    )
    inlines = (TaskInLine,)
    resource_class = UserStoryResource

    def get_readonly_fields(self, request, obj=None):
        if not obj or obj.status not in [UserStory.Status.IN_VALIDATION, UserStory.Status.COMPLETED]:
            return self.readonly_fields + ("validated",)
        return self.readonly_fields


@admin.register(Progress)
class ProgressAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "user_story", "date", "progress")
    list_select_related = ("user_story",)
    list_filter = ("date",)
    ordering = ("-date",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("user_story", "date", "progress")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    raw_id_fields = ("user_story",)
    readonly_fields = ("id", "creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = ProgressResource


@admin.register(Effort)
class EffortAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "date", "user", "role", "user_story", "effort")
    list_select_related = ("user", "user_story")
    list_filter = ("date", "user", "role")
    ordering = ("-date",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("user_story", "date", "user", "role", "effort")}),
        (_("Información extra"), {"fields": ("comments",)}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    raw_id_fields = ("user_story",)
    readonly_fields = ("id", "creation_user", "creation_datetime", "modification_user", "modification_datetime")
    resource_class = EffortResource


@admin.register(Task)
class TaskAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "user_story", "weight", "done")
    list_select_related = ("user_story",)
    list_filter = ("done",)
    ordering = ("-creation_datetime",)
    fieldsets = (
        (_("Identificación"), {"fields": ("id",)}),
        (_("Información básica"), {"fields": ("name", "user_story", "weight")}),
        (_("Estado"), {"fields": ("done", "done_changed")}),
        (
            _("Autoría"),
            {"fields": ("creation_user", "creation_datetime", "modification_user", "modification_datetime")},
        ),
    )
    raw_id_fields = ("user_story",)
    readonly_fields = (
        "id",
        "creation_user",
        "creation_datetime",
        "modification_user",
        "modification_datetime",
        "done_changed",
    )
    resource_class = TaskResource
