from datetime import date

from django.utils.translation import ugettext_lazy as _

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from ..models import Effort, Epic, Progress, Sprint, Task, UserStory, UserStoryType
from users.api.serializers import UserSerializer


class SprintSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    name = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Sprint.objects.all(), lookup="iexact")]
    )
    tags = TagListSerializerField()

    def validate(self, data):
        data = super().validate(data)
        if data.get("end_date") < data.get("start_date"):
            raise serializers.ValidationError(
                _("No es posible crear un sprint con fecha de fin anterior a la de inicio")
            )
        return data

    class Meta:
        model = Sprint
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "ongoing",
            "accountable_user",
            "num_of_user_stories",
            "current_progress",
            "tags",
        )
        read_only_fields = (
            "id",
            "ongoing",
            "num_of_user_stories",
            "current_progress",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        expandable_fields = {"accountable_user": UserSerializer}


class EpicSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    name = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Epic.objects.all(), lookup="iexact")]
    )
    tags = TagListSerializerField()

    class Meta:
        model = Epic
        fields = ("id", "name", "description", "external_reference", "num_of_user_stories", "current_progress", "tags")
        read_only_fields = (
            "id",
            "num_of_user_stories",
            "current_progress",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )


class UserStoryTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = UserStoryType
        fields = ("id", "name", "colour")
        read_only_fields = ("id",)


class ProgressSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Progress
        fields = ("id", "user_story", "date", "progress")
        read_only_fields = ("id", "creation_datetime", "creation_user", "modification_datetime", "modification_user")


class EffortSerializer(FlexFieldsModelSerializer):
    def validate(self, data):
        data = super().validate(data)
        if data.get("date") and data.get("date") > date.today():
            raise serializers.ValidationError(_("No es posible añadir esfuerzos a futuro"))
        return data

    class Meta:
        model = Effort
        fields = ("id", "date", "user", "role", "user_story", "effort", "comments", "creation_datetime")
        read_only_fields = ("id", "creation_datetime", "creation_user", "modification_datetime", "modification_user")
        expandable_fields = {"user_story": "scrum.api.serializers.UserStorySerializer"}
        validators = [
            UniqueTogetherValidator(queryset=Effort.objects.all(), fields=["date", "user", "role", "user_story"])
        ]


class TaskSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "user_story", "order", "weight", "done", "done_changed")
        read_only_fields = (
            "id",
            "order",
            "done_changed",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        expandable_fields = {"user_story": "scrum.api.serializers.UserStorySerializer"}
        validators = [UniqueTogetherValidator(queryset=Task.objects.all(), fields=["name", "user_story"])]


class UserStorySerializer(TaggitSerializer, FlexFieldsModelSerializer):
    tags = TagListSerializerField()

    def validate(self, data):
        data = super().validate(data)
        if data.get("end_date") and data.get("start_date") and data["end_date"] < data["start_date"]:
            raise serializers.ValidationError(_("Fecha de fin anterior a la de inicio"))
        if data.get("sprint"):
            if not data.get("start_date") or not data.get("end_date"):
                raise serializers.ValidationError(
                    _("Es necesario asignar fechas a las historias de usuario asignadas a un sprint")
                )
            if data["start_date"] < data["sprint"].start_date or data["start_date"] > data["sprint"].end_date:
                raise serializers.ValidationError(_("Fecha de inicio fuera del sprint"))
            if data["end_date"] < data["sprint"].start_date or data["end_date"] > data["sprint"].end_date:
                raise serializers.ValidationError(_("Fecha de fin fuera del sprint"))
            if not data.get("development_user"):
                raise serializers.ValidationError(
                    _("No es posible incluir una historia de usuario en un sprint sin un responsable asignado.")
                )
        return data

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
            "actual_effort",
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
        )
        read_only_fields = (
            "id",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
            "current_progress",
            "current_progress_changed",
            "validated_changed",
            "status",
            "actual_effort",
        )
        expandable_fields = {
            "type": UserStoryTypeSerializer,
            "epic": EpicSerializer,
            "sprint": SprintSerializer,
            "development_user": UserSerializer,
            "validation_user": UserSerializer,
            "support_user": UserSerializer,
            "progress_log": (ProgressSerializer, {"many": True}),
            "effort_allocation": (EffortSerializer, {"many": True}),
        }
        validators = [
            UniqueTogetherValidator(queryset=UserStory.objects.all(), fields=["name", "sprint"]),
            UniqueTogetherValidator(queryset=UserStory.objects.all(), fields=["name", "epic"]),
        ]


class UserStoryDeveloperSerializer(UserStorySerializer):
    class Meta(UserStorySerializer.Meta):
        read_only_fields = tuple(  # type: ignore
            field
            for field in UserStorySerializer.Meta.fields
            if field
            not in [
                "external_resource",
                "development_comments",
                "cvs_reference",
                "risk_level",
                "risk_comments",
                "use_migrations",
                "deployment_notes",
            ]
        )


class UserStoryValidatorSerializer(UserStorySerializer):
    class Meta(UserStorySerializer.Meta):
        read_only_fields = tuple(  # type: ignore
            field
            for field in UserStorySerializer.Meta.fields
            if field not in ["validated", "validation_comments", "risk_level", "risk_comments"]
        )


class UserStorySupportSerializer(UserStorySerializer):
    class Meta(UserStorySerializer.Meta):
        read_only_fields = tuple(  # type: ignore
            field
            for field in UserStorySerializer.Meta.fields
            if field not in ["support_comments", "risk_level", "risk_comments"]
        )
