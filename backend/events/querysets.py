from django.db import models
from django.db.models import Q


class EventQuerySet(models.QuerySet):
    def by_user(self, user):
        if user.is_superuser:
            return self
        return self.filter(Q(visibility="PU") | Q(attendees=user) | Q(groups__user=user) | Q(creation_user=user))

    def by_attendee(self, user):
        return self.filter(Q(attendees=user) | Q(groups__user=user))

    def important_by_attendee(self, user):
        return self.by_attendee(user).filter(type__important=True)
