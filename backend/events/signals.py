from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import make_aware

from notifications.signals import notify

from .models import Event


@receiver(pre_save, sender=Event)
def set_time_for_all_day_events(sender, instance, *args, **kwargs):
    """
    Sets max and min time in all-day events
    """
    if instance.all_day:
        instance.start_datetime = make_aware(datetime.combine(instance.start_datetime.date(), datetime.min.time()))
        instance.end_datetime = make_aware(datetime.combine(instance.end_datetime.date(), datetime.max.time()))


@receiver(m2m_changed, sender=Event.attendees.through)
@receiver(m2m_changed, sender=Event.groups.through)
def notify_attendees_of_invitation(sender, instance, action, reverse, model, pk_set, *args, **kwargs):
    """
    Notifies attendees that they have been invited to a new event
    """
    if action == "post_add" and isinstance(instance, Event) and not instance.type.system:
        notification_sender = instance.notification_sender

        recipient_qs = None
        if model == get_user_model():
            recipient_qs = model.objects.filter(pk__in=pk_set).exclude(pk=notification_sender.pk)
        elif model == Group:
            recipient_qs = (
                get_user_model().objects.filter(groups__in=pk_set).exclude(pk=notification_sender.pk).distinct()
            )

        if recipient_qs and recipient_qs.exists():
            notify.send(
                sender=notification_sender, recipient=recipient_qs, verb="te ha invitado al evento", target=instance,
            )


@receiver(post_save, sender=Event)
def notify_attendees_of_changes(sender, instance, created, *args, **kwargs):
    """
    Notifies attendees of changes made in an existent event
    """
    if not created and not instance.type.system:
        notification_sender = instance.notification_sender

        recipient_qs = (
            get_user_model()
            .objects.filter(Q(events=instance) | Q(groups__events=instance))
            .exclude(pk=notification_sender.pk)
            .distinct()
        )

        if recipient_qs.exists():
            notify.send(
                sender=notification_sender, recipient=recipient_qs, verb="ha modificado el evento", target=instance,
            )
