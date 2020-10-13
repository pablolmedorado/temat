from datetime import date

from django.db.models import Count, F, Q, Sum
from django.utils.translation import ugettext_lazy as _

from rest_flex_fields import is_expanded
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import (
    EffortFilterSet,
    EpicFilterSet,
    ProgressFilterSet,
    SprintFilterSet,
    TaskFilterSet,
    UserStoryFilterSet,
)
from .models import Effort, Epic, Progress, Sprint, Task, UserStory, UserStoryType
from .permissions import EffortPermission, TaskPermission, UserStoryPermission
from .serializers import (
    EffortSerializer,
    EpicSerializer,
    ProgressSerializer,
    SprintSerializer,
    TaskSerializer,
    UserStoryDeveloperSerializer,
    UserStorySerializer,
    UserStorySupportSerializer,
    UserStoryTypeSerializer,
    UserStoryValidatorSerializer,
)
from .utils import (
    burn_chart_data,
    effort_role_timeline_chart_data,
    effort_user_timeline_chart_data,
    gantt_chart_data,
    user_story_user_chart_data,
)
from common.mixins import AuthorshipMixin, OrderedMixin
from common.permissions import IsAdminUserOrReadOnly


class SprintApi(AuthorshipMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    serializer_class = SprintSerializer
    filterset_class = SprintFilterSet
    search_fields = ("name",)
    ordering_fields = (
        "id",
        "name",
        "start_date",
        "end_date",
        "annotated_ongoing",
        "accountable_user__acronym",
        "user_stories__count",
        "annotated_current_progress",
    )
    ordering = ("-annotated_ongoing", "-start_date")

    def get_queryset(self, *args, **kwargs):
        return (
            Sprint.objects.with_ongoing(date.today()).with_current_progress().all().prefetch_related("tags").distinct()
        )

    @action(detail=True, methods=["GET"])
    def burn_chart(self, request, *args, **kwargs):
        instance = self.get_object()
        chart_data = burn_chart_data(instance)
        return Response(chart_data)

    @action(detail=True, methods=["GET"])
    def gantt_chart(self, request, *args, **kwargs):
        instance = self.get_object()
        chart_data = gantt_chart_data(instance)
        return Response(chart_data)


class EpicApi(AuthorshipMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Epic.objects.with_current_progress().all().prefetch_related("tags").distinct()
    serializer_class = EpicSerializer
    filterset_class = EpicFilterSet
    search_fields = ("name", "description", "external_reference")
    ordering_fields = ("id", "name", "user_stories__count", "annotated_current_progress")
    ordering = ("name",)


class UserStoryTypeApi(FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = UserStoryType.objects.all()
    serializer_class = UserStoryTypeSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class UserStoryApi(AuthorshipMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, UserStoryPermission)
    queryset = UserStory.objects.with_actual_effort().prefetch_related("tags").distinct()
    serializer_class = UserStorySerializer
    filterset_class = UserStoryFilterSet
    search_fields = (
        "id",
        "name",
        "functional_description",
        "technical_description",
        "development_comments",
        "validation_comments",
        "support_comments",
        "cvs_reference",
        "risk_comments",
    )
    ordering_fields = (
        "name",
        "type__name",
        "epic",
        "sprint",
        "start_date",
        "end_date",
        "current_progress",
        "validated",
        "status",
        "planned_effort",
        "priority",
        "risk_level",
        "cvs_reference",
    )
    ordering = ("-start_date",)
    permit_list_expands = ["type", "epic", "sprint", "development_user", "validation_user", "support_user"]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        if is_expanded(self.request, "type"):
            queryset = queryset.select_related("type")
        if is_expanded(self.request, "epic"):
            queryset = queryset.select_related("epic")
        if is_expanded(self.request, "sprint"):
            queryset = queryset.select_related("sprint")
        if "sprint" in self.kwargs:
            queryset = queryset.filter(sprint_id=self.kwargs["sprint"])
        if "epic" in self.kwargs:
            queryset = queryset.filter(epic_id=self.kwargs["epic"])
        if self.action == "my_user_stories":
            return queryset.by_user(self.request.user)
        return queryset

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.request.user.is_staff:
            return serializer_class
        if self.request.method not in permissions.SAFE_METHODS and self.detail:
            instance = self.get_object()
            if self.request.user == instance.development_user:
                return UserStoryDeveloperSerializer
            if self.request.user == instance.validation_user:
                return UserStoryValidatorSerializer
            if self.request.user == instance.support_user:
                return UserStorySupportSerializer
        return serializer_class

    @action(detail=False, methods=["GET"])
    def my_user_stories(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=["PATCH"])
    def validate(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={"validated": True}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the copied instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def copy(self, request, *args, **kwargs):
        instance = self.get_object()
        copied_instance = UserStory.get_copy(instance, request.user)
        serializer = self.get_serializer(copied_instance)

        if getattr(copied_instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the copied instance.
            copied_instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def type_pie_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = (
            UserStoryType.objects.filter(user_stories__in=queryset)
            .distinct()
            .annotate(y=Count("user_stories"))
            .values("name", "y", color=F("colour"))
        )
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def effort_role_pie_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = (
            Effort.objects.filter(user_story__in=queryset)
            .order_by("role")
            .values(name=F("role"))
            .distinct()
            .annotate(y=Sum("effort"))
        )
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def user_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = user_story_user_chart_data(queryset)
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def delayed_pie_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).exclude(status=UserStory.Status.BACKLOG)
        condition = Q(status__lte=UserStory.Status.IN_VALIDATION, end_date__lt=date.today()) | Q(
            status=UserStory.Status.COMPLETED, end_date__lte=F("validated_changed")
        )
        delayed_count = queryset.filter(condition).count()
        not_delayed_count = queryset.exclude(condition).count()
        chart_data = [
            {"name": _("En fecha"), "color": "#4CAF50", "y": not_delayed_count},
            {"name": _("Retrasadas"), "color": "#FF9800", "y": delayed_count},
        ]
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def overworked_pie_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).exclude(status=UserStory.Status.BACKLOG)
        perfect_estimation_count = queryset.filter(planned_effort=F("annotated_actual_effort")).count()
        underestimated_count = queryset.filter(planned_effort__lt=F("annotated_actual_effort")).count()
        overestimated_count = queryset.filter(planned_effort__gt=F("annotated_actual_effort")).count()
        chart_data = [
            {"name": _("Estimación perfecta"), "color": "#4CAF50", "y": perfect_estimation_count},
            {"name": _("Sobreestimación"), "color": "#FF9800", "y": overestimated_count},
            {"name": _("Subestimación"), "color": "#F44336", "y": underestimated_count},
        ]
        return Response(chart_data)


class ProgressApi(AuthorshipMixin, FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filterset_class = ProgressFilterSet
    ordering_fields = ("id", "user_story", "date", "progress")
    ordering = ("user_story", "date")

    def get_queryset(self, *args, **kwargs):
        if "user_story" in self.kwargs:
            return self.queryset.filter(user_story_id=self.kwargs["user_story"])
        return self.queryset


class EffortApi(AuthorshipMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, EffortPermission)
    queryset = Effort.objects.all()
    serializer_class = EffortSerializer
    permit_list_expands = ["user_story"]
    filterset_class = EffortFilterSet
    search_fields = ("comments",)
    ordering_fields = ("id", "date", "user", "role", "user_story", "user_story__name")
    ordering = ("-date", "user_story")

    def get_queryset(self, *args, **kwargs):
        if "user_story" in self.kwargs:
            return self.queryset.filter(user_story_id=self.kwargs["user_story"])
        return self.queryset

    @action(detail=False, methods=["GET"])
    def role_timeline_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = effort_role_timeline_chart_data(queryset)
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def user_timeline_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = effort_user_timeline_chart_data(queryset)
        return Response(chart_data)


class TaskApi(AuthorshipMixin, OrderedMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, TaskPermission)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permit_list_expands = ["user_story"]
    filterset_class = TaskFilterSet
    search_fields = ("name",)
    ordering_fields = ("id", "user_story", "order", "weight", "done", "done_changed")
    ordering = ("order",)

    def get_queryset(self, *args, **kwargs):
        if "user_story" in self.kwargs:
            return self.queryset.filter(user_story_id=self.kwargs["user_story"])
        return self.queryset

    @action(detail=True, methods=["PATCH"])
    def toggle(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={"done": not instance.done}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
