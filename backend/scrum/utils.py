from datetime import date, timedelta
from typing import Dict, List

import pydash

from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q, QuerySet, Sum
from django.utils.translation import ugettext_lazy as _

from .models import Effort, Progress, Sprint, UserStory


def burn_chart_data(instance: Sprint) -> Dict:
    sprint_dates = [
        instance.start_date + timedelta(days=num_of_days)
        for num_of_days in range((instance.end_date - instance.start_date).days + 1)
    ]
    user_stories_count = instance.user_stories.count()
    if not user_stories_count:
        result = [
            {"date": str(sprint_date), "effort_burned": None, "current_effort": None} for sprint_date in sprint_dates
        ]
        return {"total_effort": 0, "data": result}
    else:
        total_effort = instance.user_stories.aggregate(Sum("planned_effort"))["planned_effort__sum"]
        user_stories = instance.user_stories.values("id", "planned_effort")
        progress_records = (
            Progress.objects.filter(user_story__sprint=instance)
            .order_by("user_story_id", "date")
            .values("user_story_id", "date", "progress")
        )
        for user_story in user_stories:
            user_story["progress_data"] = []
            user_story_progress_dict = {
                str(record["date"]): record
                for record in progress_records
                if record["user_story_id"] == user_story["id"]
            }
            for date_index, sprint_date in enumerate(sprint_dates):
                if str(sprint_date) in user_story_progress_dict:
                    progress = user_story_progress_dict[str(sprint_date)]["progress"]
                elif date_index:
                    progress = user_story["progress_data"][date_index - 1] if sprint_date <= date.today() else None
                else:
                    previous_progress_records = list(
                        filter(
                            lambda progress, sprint_date=sprint_date: progress["date"] < sprint_date,
                            list(user_story_progress_dict.values()),
                        )
                    )
                    progress = previous_progress_records[-1]["progress"] if len(previous_progress_records) else 0
                user_story["progress_data"].append(progress)

        effort_records = (
            Effort.objects.filter(
                user_story__sprint=instance, date__gte=instance.start_date, date__lte=instance.end_date
            )
            .order_by("date")
            .values("date")
            .annotate(Sum("effort"))
        )

        chart_data = []
        for date_index, sprint_date in enumerate(sprint_dates):
            item = {"date": str(sprint_date), "effort_burned": None, "current_effort": None}
            effort = None
            for user_story in user_stories:
                progress = user_story["progress_data"][date_index]
                if progress is not None:
                    effort_increment = user_story["planned_effort"] if progress == 100 else 0
                    if effort is not None:
                        effort += effort_increment
                    else:
                        effort = effort_increment
            item["effort_burned"] = effort
            effort_record = next(
                filter(lambda effort, sprint_date=sprint_date: effort["date"] == sprint_date, effort_records), None
            )
            item["current_effort"] = effort_record["effort__sum"] if effort_record else 0
            chart_data.append(item)
        return {"total_effort": total_effort, "data": chart_data}


def gantt_chart_data(instance: Sprint) -> Dict:
    return {
        "name": instance.name,
        "start_date": instance.start_date,
        "end_date": instance.end_date,
        "user_stories": instance.user_stories.values(
            "id", "name", "start_date", "end_date", "current_progress", "validated", "risk_level"
        ).order_by("start_date"),
    }


def user_story_user_chart_data(queryset: QuerySet) -> Dict:
    user_base_queryset = get_user_model().objects.active().order_by().distinct()

    developers_queryset = user_base_queryset.filter(developed_user_stories__in=queryset)
    development_queryset = developers_queryset.annotate(development=Count("developed_user_stories")).values(
        "acronym", "development"
    )
    development_data = {item["acronym"]: item["development"] for item in development_queryset}

    validators_queryset = user_base_queryset.filter(validated_user_stories__in=queryset)
    validation_queryset = validators_queryset.annotate(validation=Count("validated_user_stories")).values(
        "acronym", "validation"
    )
    validation_data = {item["acronym"]: item["validation"] for item in validation_queryset}

    supporters_queryset = user_base_queryset.filter(supported_user_stories__in=queryset)
    support_queryset = supporters_queryset.annotate(support=Count("supported_user_stories")).values(
        "acronym", "support"
    )
    support_data = {item["acronym"]: item["support"] for item in support_queryset}

    user_list = list(
        developers_queryset.union(validators_queryset, supporters_queryset).values_list("acronym", flat=True)
    )
    user_list.sort()

    return {
        "categories": user_list,
        "series": [
            {"name": _("Desarrollador"), "data": [development_data.get(item, 0) for item in user_list]},
            {"name": _("Validador"), "data": [validation_data.get(item, 0) for item in user_list]},
            {"name": _("Soporte"), "data": [support_data.get(item, 0) for item in user_list]},
        ],
    }


def user_story_delayed_pie_chart_data(queryset: QuerySet) -> List:
    queryset = queryset.exclude(status=UserStory.Status.BACKLOG)
    condition = Q(status__lte=UserStory.Status.IN_VALIDATION, end_date__lt=date.today()) | Q(
        status=UserStory.Status.COMPLETED, end_date__lte=F("validated_changed")
    )
    delayed_count = queryset.filter(condition).count()
    not_delayed_count = queryset.exclude(condition).count()
    return [
        {"name": _("En fecha"), "color": "#4CAF50", "y": not_delayed_count},
        {"name": _("Retrasadas"), "color": "#FF9800", "y": delayed_count},
    ]


def user_story_overworked_pie_chart_data(queryset: QuerySet) -> List:
    queryset = queryset.exclude(status=UserStory.Status.BACKLOG)
    acceptable_estimation_count = queryset.filter(
        annotated_current_effort__gte=F("planned_effort") * 0.9, annotated_current_effort__lte=F("planned_effort") * 1.1
    ).count()
    underestimated_count = queryset.filter(annotated_current_effort__gt=F("planned_effort") * 1.1).count()
    overestimated_count = queryset.filter(annotated_current_effort__lt=F("planned_effort") * 0.9).count()
    return [
        {"name": _("Estimación aceptable (+-10%)"), "color": "#4CAF50", "y": acceptable_estimation_count},
        {"name": _("Sobreestimación (>10%)"), "color": "#FF9800", "y": overestimated_count},
        {"name": _("Subestimación (<10%)"), "color": "#F44336", "y": underestimated_count},
    ]


def effort_role_timeline_chart_data(queryset: QuerySet) -> Dict:
    queryset_values = queryset.order_by("date").values("date", "role").annotate(total_effort=Sum("effort"))
    items_by_role = pydash.group_by(queryset_values, "role")
    return {role: items_by_role[role] for role in items_by_role.keys()}


def effort_user_timeline_chart_data(queryset: QuerySet) -> Dict:
    queryset_values = queryset.order_by("date").values("date", "user__acronym").annotate(total_effort=Sum("effort"))
    items_by_user = pydash.group_by(queryset_values, "user__acronym")
    return {user__acronym: items_by_user[user__acronym] for user__acronym in items_by_user.keys()}
