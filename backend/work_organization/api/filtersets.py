import django_filters
from django_filters import DateFilter

from django.utils.translation import gettext as _

from ..models import GreenWorkingDay, Holiday, SupportWorkingDay


class GreenWorkingDayFilterSet(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GreenWorkingDay
        fields = {
            "id": ["exact", "in"],
            "date": ["exact", "gte", "lte", "year"],
            "users__id": ["exact", "in"],
            "volunteers__id": ["exact", "in"],
        }


class SupportWorkingDayFilterSet(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SupportWorkingDay
        fields = {"id": ["exact", "in"], "user_id": ["exact", "in"], "date": ["exact", "gte", "lte", "year"]}


class HolidayFilterSet(django_filters.rest_framework.FilterSet):
    expiration_date__gte = DateFilter(
        field_name="expiration_date_annotation", label=_("fecha de expiración"), lookup_expr="gte"
    )
    expiration_date__lte = DateFilter(
        field_name="expiration_date_annotation", label=_("fecha de expiración"), lookup_expr="lte"
    )

    class Meta:
        model = Holiday
        fields = {
            "id": ["exact", "in"],
            "user_id": ["exact", "in"],
            "type_id": ["exact", "in"],
            "allowance_date": ["exact", "gte", "lte", "year"],
            "planned_date": ["exact", "gte", "lte", "year", "isnull"],
            "approved": ["exact", "isnull"],
        }
