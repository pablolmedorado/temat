from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


class UserStoryContainer(models.Model):
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

    class Meta:
        abstract = True
