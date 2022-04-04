import operator
from datetime import date
from functools import reduce

from django.db.models import F, Q
from django.utils.translation import ugettext_lazy as _

from django_filters import BaseInFilter, BooleanFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from ..models import Effort, Epic, Progress, Sprint, Task, UserStory


class NumericInFilter(NumberFilter, BaseInFilter):
    pass


class SprintFilterSet(FilterSet):
    ongoing = BooleanFilter(label=_("En curso"), field_name="annotated_ongoing", lookup_expr="exact")

    class Meta:
        model = Sprint
        fields = {
            "id": ["exact", "in"],
            "name": ["icontains"],
            "start_date": ["exact", "gte", "lte"],
            "end_date": ["exact", "gte", "lte"],
            "accountable_user_id": ["exact", "in"],
            "tags__name": ["in", "iexact", "icontains", "istartswith"],
        }


class EpicFilterSet(FilterSet):
    finished = BooleanFilter(label=_("Finalizada"), method="finished_filter")
    current_progress__gte = NumberFilter(
        label=_("Avance actual mayor o igual que"), field_name="annotated_current_progress", lookup_expr="gte"
    )
    current_progress__lte = NumberFilter(
        label=_("Avance actual menor o igual que"), field_name="annotated_current_progress", lookup_expr="lte"
    )

    def finished_filter(self, queryset, field_name, value):
        condition = Q(annotated_current_progress=100)
        if value is True:
            return queryset.filter(condition)
        elif value is False:
            return queryset.exclude(condition)
        else:
            return queryset

    class Meta:
        model = Epic
        fields = {
            "id": ["exact", "in"],
            "name": ["icontains"],
            "description": ["icontains"],
            "external_reference": ["icontains"],
            "tags__name": ["in", "iexact", "icontains", "istartswith"],
        }


class UserStoryFilterSet(FilterSet):
    delayed = BooleanFilter(label=_("Retrasada"), method="delayed_filter")
    overworked = BooleanFilter(label=_("Con sobreesfuerzo"), method="overworked_filter")
    any_role_user__in = NumericInFilter(label=_("Usuario en cualquier rol"), method="any_role_user_filter")

    def delayed_filter(self, queryset, field_name, value):
        condition = Q(status__lte=3, end_date__lt=date.today()) | Q(status__gte=4, end_date__lte=F("validated_changed"))
        if value is True:
            return queryset.filter(condition)
        elif value is False:
            return queryset.exclude(condition)
        else:
            return queryset

    def overworked_filter(self, queryset, field_name, value):
        condition = Q(planned_effort__lt=F("annotated_current_effort"))
        if value is True:
            return queryset.filter(condition)
        elif value is False:
            return queryset.exclude(condition)
        else:
            return queryset

    def any_role_user_filter(self, queryset, field_name, value):
        filters = [(Q(development_user_id=id) | Q(validation_user_id=id) | Q(support_user_id=id)) for id in value]
        return queryset.filter(reduce(operator.or_, filters))

    class Meta:
        model = UserStory
        fields = {
            "id": ["exact", "in"],
            "name": ["icontains"],
            "type_id": ["exact", "in"],
            "epic_id": ["exact", "in"],
            "sprint_id": ["exact", "in"],
            "sprint__start_date": ["exact", "gte", "lte", "year"],
            "sprint__end_date": ["exact", "gte", "lte", "year"],
            "functional_description": ["icontains"],
            "technical_description": ["icontains"],
            "external_resource": ["icontains"],
            "start_date": ["exact", "gte", "lte", "year"],
            "end_date": ["exact", "gte", "lte", "year"],
            "current_progress": ["exact", "gte", "lte"],
            "current_progress_changed": ["exact", "gte", "lte", "year", "date", "date__lte", "date__gte"],
            "validated": ["exact", "isnull"],
            "validated_changed": ["exact", "gte", "lte", "year", "date", "date__lte", "date__gte"],
            "status": ["exact", "in", "gte", "lte"],
            "planned_effort": ["exact", "gte", "lte"],
            "priority": ["exact", "in", "gte", "lte"],
            "development_user_id": ["exact", "in"],
            "validation_user_id": ["exact", "in"],
            "support_user_id": ["exact", "in"],
            "cvs_branch_name": ["exact", "icontains"],
            "cvs_issue_id": ["exact", "in", "gte", "lte"],
            "cvs_pull_request_id": ["exact", "in", "gte", "lte"],
            "risk_level": ["exact", "in"],
            "use_migrations": ["exact"],
            "tags__name": ["in", "iexact", "icontains", "istartswith"],
        }


class ProgressFilterSet(FilterSet):
    class Meta:
        model = Progress
        fields = {
            "id": ["exact", "in"],
            "user_story_id": ["exact", "in"],
            "date": ["exact", "gte", "lte"],
            "progress": ["exact", "gte", "lte"],
        }


class EffortFilterSet(FilterSet):
    class Meta:
        model = Effort
        fields = {
            "id": ["exact", "in"],
            "date": ["exact", "gte", "lte"],
            "user_id": ["exact", "in"],
            "role": ["exact", "in"],
            "user_story_id": ["exact", "in"],
            "effort": ["exact", "gte", "lte"],
        }


class TaskFilterSet(FilterSet):
    class Meta:
        model = Task
        fields = {
            "id": ["exact", "in"],
            "user_story_id": ["exact", "in"],
            "weight": ["exact", "gte", "lte"],
            "done": ["exact"],
        }
