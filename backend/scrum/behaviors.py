from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


class UserStoryContainer(models.Model):
    class Meta:
        abstract = True

    @property
    def num_of_user_stories(self):
        if hasattr(self, "user_stories__count"):
            return self.user_stories__count
        return self.user_stories.count()

    @property
    def current_progress(self):
        if hasattr(self, "annotated_current_progress"):
            return self.annotated_current_progress
        if self.user_stories.exists():
            current_progress = self.user_stories.all().aggregate(
                current_progress__sum=Coalesce(Sum("current_progress"), Value(0))
            )
            return current_progress["current_progress__sum"] // self.user_stories.count()
        return 0

    @property
    def planned_effort(self):
        if hasattr(self, "annotated_planned_effort"):
            return self.annotated_planned_effort
        if self.user_stories.exists():
            planned_effort = self.user_stories.all().aggregate(
                planned_effort__sum=Coalesce(Sum("planned_effort"), Value(0))
            )
            return planned_effort["planned_effort__sum"]
        return 0

    @property
    def current_effort(self):
        if hasattr(self, "annotated_current_effort"):
            return self.annotated_current_effort
        if self.user_stories.exists():
            current_effort = self.user_stories.all().aggregate(
                current_effort__sum=Coalesce(Sum("effort_allocation__effort"), Value(0))
            )
            return current_effort["current_effort__sum"]
        return 0
