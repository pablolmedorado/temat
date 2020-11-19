from rest_framework.decorators import action
from rest_framework.response import Response


class FlatDatesMixin:
    flat_dates_field = "date"

    @action(detail=False, methods=["GET"])
    def flat_dates(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        flat_dates = (
            queryset.exclude(**{f"{self.flat_dates_field}__isnull": True})
            .order_by(self.flat_dates_field)
            .values_list(self.flat_dates_field, flat=True)
            .distinct()
        )
        return Response(flat_dates)
