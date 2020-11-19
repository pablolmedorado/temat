from django_filters.rest_framework import FilterSet

from ..models import Event


class EventFilterSet(FilterSet):
    class Meta:
        model = Event
        fields = {
            "id": ["exact", "in"],
            "name": ["icontains"],
            "details": ["icontains"],
            "start_datetime": ["exact", "gte", "lte", "year", "date", "date__lte", "date__gte"],
            "end_datetime": ["exact", "gte", "lte", "year", "date", "date__lte", "date__gte"],
            "all_day": ["exact"],
            "visibility": ["exact"],
            "attendees__id": ["exact", "in"],
            "groups__id": ["exact", "in"],
            "type_id": ["exact", "in"],
            "type__important": ["exact"],
            "type__system": ["exact"],
            "tags__name": ["in", "iexact", "icontains", "istartswith"],
        }
