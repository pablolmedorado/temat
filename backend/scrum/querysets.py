from django.db import models
from django.db.models import Case, Count, ExpressionWrapper, F, Q, Sum, Value, When
from django.db.models.functions import Cast, Coalesce


class UserStoryContainerQuerySet(models.QuerySet):
    def with_current_progress(self):
        return (
            self.annotate(current_progress__sum=Coalesce(Sum("user_stories__current_progress"), Value(0)))
            .annotate(user_stories__count=Count("user_stories"))
            .annotate(
                annotated_current_progress=Case(
                    When(Q(user_stories__count=0), then=0),
                    default=ExpressionWrapper(
                        Cast(F("current_progress__sum") / F("user_stories__count"), models.PositiveSmallIntegerField()),
                        output_field=models.PositiveSmallIntegerField(),
                    ),
                    output_field=models.PositiveSmallIntegerField(),
                )
            )
        )

    def with_effort(self):
        return self.annotate(
            annotated_planned_effort=Coalesce(Sum("user_stories__planned_effort"), Value(0)),
            annotated_current_effort=Coalesce(Sum("user_stories__effort_allocation__effort"), Value(0)),
        )


class SprintQuerySet(UserStoryContainerQuerySet):
    def with_ongoing(self, reference_date):
        return self.annotate(
            annotated_ongoing=models.Case(
                models.When(Q(start_date__lte=reference_date, end_date__gte=reference_date), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        )


class EpicQuerySet(UserStoryContainerQuerySet):
    pass


class UserStoryQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(Q(development_user=user) | Q(validation_user=user) | Q(support_user=user))

    def with_current_effort(self):
        return self.annotate(annotated_current_effort=Coalesce(Sum("effort_allocation__effort"), Value(0)))
