from django.contrib.auth import get_user_model

from django_currentuser.middleware import get_current_authenticated_user
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Effort, Epic, Progress, Sprint, Task, UserStory, UserStoryType


class SprintResource(resources.ModelResource):
    accountable_user = Field(
        attribute="accountable_user", widget=ForeignKeyWidget(model=get_user_model(), field="username"), readonly=False
    )

    class Meta:
        model = Sprint
        fields = ("id", "name", "start_date", "end_date", "accountable_user")
        export_order = fields


class EpicResource(resources.ModelResource):
    class Meta:
        model = Epic
        fields = ("id", "name", "description", "external_reference")
        export_order = fields


class UserStoryTypeResource(resources.ModelResource):
    class Meta:
        model = UserStoryType
        fields = ("id", "name", "colour")
        export_order = fields


class UserStoryResource(resources.ModelResource):
    type = Field(attribute="type", widget=ForeignKeyWidget(model=UserStoryType, field="name"), readonly=False)
    development_user = Field(
        attribute="development_user", widget=ForeignKeyWidget(model=get_user_model(), field="username"), readonly=False
    )
    validation_user = Field(
        attribute="validation_user", widget=ForeignKeyWidget(model=get_user_model(), field="username"), readonly=False
    )
    support_user = Field(
        attribute="support_user", widget=ForeignKeyWidget(model=get_user_model(), field="username"), readonly=False
    )
    creation_user = Field(
        attribute="creation_user",
        widget=ForeignKeyWidget(model=get_user_model(), field="username"),
        readonly=False,
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
            "start_date",
            "end_date",
            "validated",
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
            "creation_user",
        )
        export_order = fields


class ProgressResource(resources.ModelResource):
    class Meta:
        model = Progress
        fields = ("id", "user_story", "date", "progress")
        export_order = fields


class EffortResource(resources.ModelResource):
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="username"), readonly=False)

    class Meta:
        model = Effort
        fields = ("id", "date", "user", "role", "user_story", "effort", "comments")
        export_order = fields


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        fields = ("id", "name", "user_story", "weight", "done")
        export_order = fields
