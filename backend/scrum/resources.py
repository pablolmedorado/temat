from django.contrib.auth import get_user_model

from django_currentuser.middleware import get_current_authenticated_user
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Effort, Epic, Progress, Sprint, Task, UserStory, UserStoryType
from common.widgets import TagsWidget


class SprintResource(resources.ModelResource):
    accountable_user = Field(
        attribute="accountable_user", widget=ForeignKeyWidget(model=get_user_model(), field="username")
    )
    tags = Field(attribute="tags", widget=TagsWidget())

    class Meta:
        model = Sprint
        fields = ("id", "name", "start_date", "end_date", "accountable_user", "tags")
        export_order = fields


class EpicResource(resources.ModelResource):
    tags = Field(attribute="tags", widget=TagsWidget())

    class Meta:
        model = Epic
        fields = ("id", "name", "description", "external_reference", "tags")
        export_order = fields


class UserStoryTypeResource(resources.ModelResource):
    class Meta:
        model = UserStoryType
        fields = ("id", "name", "colour")
        export_order = fields


class UserStoryResource(resources.ModelResource):
    type = Field(attribute="type", widget=ForeignKeyWidget(model=UserStoryType, field="name"))
    epic = Field(attribute="epic", widget=ForeignKeyWidget(model=Epic, field="name"))
    sprint = Field(attribute="sprint", widget=ForeignKeyWidget(model=Sprint, field="name"))
    current_progress = Field(attribute="current_progress", readonly=True)
    current_progress_changed = Field(attribute="current_progress_changed", readonly=True)
    validated_changed = Field(attribute="validated_changed", readonly=True)
    status = Field(attribute="status", readonly=True)
    development_user = Field(
        attribute="development_user", widget=ForeignKeyWidget(model=get_user_model(), field="username")
    )
    validation_user = Field(
        attribute="validation_user", widget=ForeignKeyWidget(model=get_user_model(), field="username")
    )
    support_user = Field(attribute="support_user", widget=ForeignKeyWidget(model=get_user_model(), field="username"))
    tags = Field(attribute="tags", widget=TagsWidget())
    creation_user = Field(
        attribute="creation_user",
        widget=ForeignKeyWidget(model=get_user_model(), field="username"),
        default=get_current_authenticated_user,
    )
    modification_user = Field(
        attribute="modification_user",
        widget=ForeignKeyWidget(model=get_user_model(), field="username"),
        default=get_current_authenticated_user,
    )

    class Meta:
        model = UserStory
        fields = (
            "id",
            "name",
            "type",
            "epic",
            "sprint",
            "functional_description",
            "technical_description",
            "external_resource",
            "start_date",
            "end_date",
            "current_progress",
            "current_progress_changed",
            "validated",
            "validated_changed",
            "status",
            "planned_effort",
            "priority",
            "development_user",
            "development_comments",
            "validation_user",
            "validation_comments",
            "support_user",
            "support_comments",
            "cvs_reference",
            "risk_level",
            "risk_comments",
            "use_migrations",
            "deployment_notes",
            "tags",
            "creation_user",
            "creation_datetime",
            "modification_user",
            "modification_datetime",
        )
        export_order = fields


class ProgressResource(resources.ModelResource):
    class Meta:
        model = Progress
        fields = ("id", "user_story", "date", "progress")
        export_order = fields


class EffortResource(resources.ModelResource):
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="username"))

    class Meta:
        model = Effort
        fields = ("id", "date", "user", "role", "user_story", "effort", "comments")
        export_order = fields


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        fields = ("id", "name", "user_story", "weight", "done")
        export_order = fields
