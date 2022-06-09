from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import EventType
from .models import User


@receiver(post_save, sender=User)
def update_calendar_event_names(sender, instance, created, raw, *args, **kwargs):
    """
    Updates support & holidays calendar event names in case user acronym had changed
    """
    if not created:
        instance.events.filter(
            type__system_slug__in=[EventType.SystemSlug.SUPPORT, EventType.SystemSlug.HOLIDAY]
        ).update(name=instance.acronym)
