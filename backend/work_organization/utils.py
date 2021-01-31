from typing import Dict

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, QuerySet
from django.utils.translation import ugettext_lazy as _


def user_availability_chart_data(queryset: QuerySet) -> Dict:
    available_holidays_queryset = (
        queryset.filter(Q(planned_date__isnull=True) | Q(approved=False))
        .order_by("user__acronym")
        .values("user__acronym")
        .distinct()
        .annotate(count=Count("id"))
    )
    planned_holidays_queryset = (
        queryset.filter(planned_date__isnull=False, approved=True)
        .order_by("user__acronym")
        .values("user__acronym")
        .distinct()
        .annotate(count=Count("id"))
    )

    available_holidays_data = {item["user__acronym"]: item["count"] for item in available_holidays_queryset}
    planned_holidays_data = {item["user__acronym"]: item["count"] for item in planned_holidays_queryset}

    user_model = get_user_model()
    user_list = (
        user_model.objects.active().exclude(company__isnull=True).order_by("acronym").values_list("acronym", flat=True)
    )

    chart_data = {
        "categories": user_list,
        "series": [
            {"name": _("Disponibles"), "data": [available_holidays_data.get(item, 0) for item in user_list]},
            {"name": _("Planificadas"), "data": [planned_holidays_data.get(item, 0) for item in user_list]},
        ],
    }

    return chart_data


def green_working_day_user_chart_data(queryset: QuerySet) -> Dict:
    user_list = (
        get_user_model()
        .objects.active()
        .filter(Q(green_working_days_as_main__in=queryset) | Q(green_working_days_as_support__in=queryset))
        .order_by("acronym")
        .distinct()
        .values_list("acronym", flat=True)
    )

    main_queryset = (
        get_user_model()
        .objects.active()
        .filter(green_working_days_as_main__in=queryset)
        .annotate(main=Count("green_working_days_as_main"))
        .values("acronym", "main")
    )
    main_data = {item["acronym"]: item["main"] for item in main_queryset}
    support_queryset = (
        get_user_model()
        .objects.active()
        .filter(green_working_days_as_support__in=queryset)
        .annotate(support=Count("green_working_days_as_support"))
        .values("acronym", "support")
    )
    support_data = {item["acronym"]: item["support"] for item in support_queryset}

    chart_data = {
        "categories": user_list,
        "series": [
            {"name": _("Principal"), "data": [main_data.get(item, 0) for item in user_list]},
            {"name": _("Apoyo"), "data": [support_data.get(item, 0) for item in user_list]},
        ],
    }

    return chart_data


def support_working_day_user_chart_data(queryset: QuerySet) -> Dict:
    queryset_result = (
        get_user_model()
        .objects.active()
        .filter(support_working_days__in=queryset)
        .distinct()
        .annotate(count=Count("support_working_days"))
        .order_by("acronym")
        .values("acronym", "count")
    )

    chart_data: Dict = {"categories": [], "data": []}
    for item in queryset_result:
        chart_data["categories"].append(item["acronym"])
        chart_data["data"].append(item["count"])

    return chart_data
