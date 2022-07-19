from statistics import mean
from typing import Any, Dict

import pydash

from django.db.models import Count, QuerySet
from django.db.models.functions import TruncMonth

from .models import EventType


def monthly_chart_data(queryset: QuerySet) -> Dict:
    series_queryset = EventType.objects.filter(events__in=queryset).distinct().order_by("name").values("name", "colour")
    series_dict = {
        item["name"]: {"name": item["name"], "color": item["colour"], "data": []} for item in series_queryset
    }

    chart_data: Dict[str, Any] = {"categories": [], "series": []}
    data_queryset = (
        queryset.annotate(datetime=TruncMonth("start_datetime"))
        .order_by("datetime", "type__name")
        .values("datetime", "type__name")
        .distinct()
        .annotate(count=Count("id"))
    )
    data_dict = [{**item, "month": item["datetime"].strftime("%Y-%m")} for item in data_queryset]

    structured_data_dict = pydash.group_by(data_dict, "month")
    for month, data in structured_data_dict.items():
        structured_data_dict[month] = pydash.group_by(data, "type__name")

    chart_data["categories"] = list(structured_data_dict.keys())
    for category in chart_data["categories"]:
        event_types = structured_data_dict[category].keys()
        for event_type, serie in series_dict.items():
            if event_type in event_types:
                series_dict[event_type]["data"].append(structured_data_dict[category][event_type][0]["count"])
            else:
                series_dict[event_type]["data"].append(None)
    chart_data["series"] = list(series_dict.values())

    average_data = []
    for index in range(len(chart_data["categories"])):
        truly_values = pydash.compact([serie["data"][index] for serie in chart_data["series"]])
        average_data.append(sum(truly_values))
    chart_data["average"] = mean(average_data) if len(average_data) else None

    return chart_data
