from django.db import models
from django.db.models import DateField, ExpressionWrapper, F


class HolidayQuerySet(models.QuerySet):
    def with_expiration_date(self):
        return self.select_related("type").annotate(
            expiration_date_annotation=ExpressionWrapper(
                F("allowance_date") + F("type__validity"), output_field=DateField()
            )
        )

    def available(self, now):
        return self.with_expiration_date().filter(planned_date__isnull=True, expiration_date_annotation__gt=now)
