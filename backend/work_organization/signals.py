from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import make_aware

from notifications.signals import notify

from .models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay
from common.utils import get_notification_sender, notify_item_assignation_to_user
from events.models import Event, EventType


@receiver(post_save, sender=Holiday)
def create_or_update_holiday_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the holiday
    """
    holiday_ct = ContentType.objects.get_for_model(Holiday)
    if instance.approved and instance.planned_date:
        event_type = EventType.objects.get(system_slug=EventType.SystemSlug.HOLIDAY)
        obj, obj_created = Event.objects.update_or_create(
            link_content_type=holiday_ct,
            link_object_id=instance.id,
            defaults={
                "start_datetime": make_aware(datetime.combine(instance.planned_date, datetime.min.time())),
                "end_datetime": make_aware(datetime.combine(instance.planned_date, datetime.max.time())),
                "all_day": True,
                "type": event_type,
                "name": instance.user.acronym,
            },
        )
        obj.attendees.set([instance.user])
    else:
        Event.objects.filter(link_content_type=holiday_ct, link_object_id=instance.id).delete()


@receiver(pre_save, sender=Holiday)
def notify_user_of_holiday_status(sender, instance, *args, **kwargs):
    """
    Notifies an user that a holiday has changed its status
    """
    if instance.persisted and instance.planned_date and instance.approved is not None:
        old_instance = Holiday.objects.get(pk=instance.id)

        if instance.approved != old_instance.approved:
            notification_sender = get_notification_sender()

            if notification_sender != instance.user:
                level = "success" if instance.approved else "warning"
                notification_verb = "aprobado" if instance.approved else "rechazado"
                notify.send(
                    sender=notification_sender,
                    recipient=instance.user,
                    level=level,
                    verb=f"ha {notification_verb} tu día de vacaciones",
                    target=instance,
                )


@receiver(post_save, sender=SupportWorkingDay)
def create_or_update_support_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the support working day
    """
    event_type = EventType.objects.get(system_slug=EventType.SystemSlug.SUPPORT)
    obj, obj_created = Event.objects.update_or_create(
        link_content_type=ContentType.objects.get_for_model(SupportWorkingDay),
        link_object_id=instance.id,
        defaults={
            "start_datetime": make_aware(datetime.combine(instance.date, datetime.min.time())),
            "end_datetime": make_aware(datetime.combine(instance.date, datetime.max.time())),
            "all_day": True,
            "type": event_type,
            "name": instance.user.acronym,
        },
    )
    obj.attendees.set([instance.user])


@receiver(pre_save, sender=SupportWorkingDay)
def notify_users_of_existing_support_assignation(sender, instance, *args, **kwargs):
    """
    Notifies an user that has been assigned to an existing Support Working Day
    """
    if instance.persisted:
        old_instance = SupportWorkingDay.objects.get(pk=instance.id)
        notify_item_assignation_to_user(instance, "user", "te ha asignado la jornada de soporte", old_instance)


@receiver(post_save, sender=SupportWorkingDay)
def notify_users_of_new_support_assignation(sender, instance, created, *args, **kwargs):
    """
    Notifies an user that has been assigned to a new Support Working Day
    """
    if created:
        notify_item_assignation_to_user(instance, "user", "te ha asignado la jornada de soporte")


@receiver(post_save, sender=GreenWorkingDay)
def create_or_update_green_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the green working day
    """
    greenworkingday_ct = ContentType.objects.get_for_model(GreenWorkingDay)
    event_type = EventType.objects.get(system_slug=EventType.SystemSlug.GREEN)
    Event.objects.update_or_create(
        link_content_type=greenworkingday_ct,
        link_object_id=instance.id,
        defaults={
            "start_datetime": make_aware(datetime.combine(instance.date, datetime.min.time())),
            "end_datetime": make_aware(datetime.combine(instance.date, datetime.max.time())),
            "all_day": True,
            "type": event_type,
            "name": instance.label,
        },
    )


@receiver(m2m_changed, sender=GreenWorkingDay.users.through)
def on_green_users_change(sender, instance, action, reverse, model, pk_set, using, *args, **kwargs):
    """
    Manages event attendees, holidays and notification when green working days
    users are added or removed
    """
    # GreenWorkingDay -> User
    if not reverse:
        # Event management
        if action in ["post_add", "post_remove"]:
            event = instance.events.first()
            event.attendees.set(instance.users.all())
        # Holiday management
        if action == "post_add":
            holiday_type = HolidayType.objects.get(system_slug=HolidayType.SystemSlug.GREEN)
            affected_users = get_user_model().objects.filter(id__in=pk_set)
            for user in affected_users:
                if user.company and user.company.extra_holiday_with_green_working_days:
                    Holiday.objects.update_or_create(
                        user_id=user.id,
                        green_working_day_id=instance.id,
                        defaults={"type": holiday_type, "allowance_date": instance.date},
                    )
                else:
                    Holiday.objects.filter(user_id=user.id, green_working_day_id=instance.id).delete()
        if action in ["post_remove", "post_clear"]:
            Holiday.objects.filter(green_working_day_id=instance.id).exclude(user__in=instance.users.all()).delete()
        # Notification
        if action == "post_add":
            notification_sender = get_notification_sender()
            affected_users = get_user_model().objects.filter(id__in=pk_set)
            notify.send(
                sender=notification_sender,
                recipient=affected_users.exclude(pk=notification_sender.pk),
                verb="te ha asignado la jornada especial",
                target=instance,
            )

    # User -> GreenWorkingDay
    else:
        # Event management
        if action in ["post_add", "post_remove", "post_clear"]:
            greenworkingday_ct = ContentType.objects.get_for_model(GreenWorkingDay)
            events = Event.objects.filter(link_content_type=greenworkingday_ct)
            if pk_set:
                events = events.filter(link_object_id__in=pk_set)
            if action == "post_add":
                instance.events.add(*events)
            if action in ["post_remove", "post_clear"]:
                instance.events.remove(*events)
        # Holiday management
        if action == "post_add":
            holiday_type = HolidayType.objects.get(system_slug=HolidayType.SystemSlug.GREEN)
            if instance.company and instance.company.extra_holiday_with_green_working_days:
                affected_greendays = GreenWorkingDay.objects.filter(id__in=pk_set)
                for greenday in affected_greendays:
                    instance.holidays.update_or_create(
                        green_working_day_id=greenday.id,
                        defaults={"type": holiday_type, "allowance_date": greenday.date},
                    )
            else:
                instance.holidays.filter(green_working_day_id__in=pk_set).delete()
        if action == "post_remove":
            instance.holidays.filter(green_working_day_id__in=pk_set).delete()
        if action == "post_clear":
            instance.holidays.filter(green_working_day_id__isnull=False).delete()
        # Notification
        if action == "post_add":
            notification_sender = get_notification_sender()
            affected_greendays = GreenWorkingDay.objects.filter(id__in=pk_set)
            for greenday in affected_greendays:
                notify.send(
                    sender=notification_sender,
                    recipient=get_user_model().objects.filter(pk=instance.id).exclude(pk=notification_sender.pk),
                    verb="te ha asignado la jornada especial",
                    target=greenday,
                )
