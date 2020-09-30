from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import make_aware

from notifications.signals import notify

from events.models import Event, EventType
from .models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay


@receiver(post_save, sender=Holiday)
def create_or_update_holiday_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the holiday
    """
    holiday_ct = ContentType.objects.get_for_model(Holiday)
    if instance.approved and instance.planned_date:
        event_type = EventType.objects.get(pk=EventType.SystemType.HOLIDAY)
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
            notification_sender = instance.notification_sender

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
    event_type = EventType.objects.get(pk=EventType.SystemType.SUPPORT)
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
        notification_sender = instance.notification_sender

        if instance.user and instance.user != notification_sender and old_instance.user != instance.user:
            notify.send(
                sender=notification_sender,
                recipient=instance.user,
                verb="te ha asignado la jornada de soporte",
                target=instance,
            )


@receiver(post_save, sender=SupportWorkingDay)
def notify_users_of_new_support_assignation(sender, instance, created, *args, **kwargs):
    """
    Notifies an user that has been assigned to an new Support Working Day
    """
    if created:
        notification_sender = instance.notification_sender

        if instance.user and instance.user != notification_sender:
            notify.send(
                sender=notification_sender,
                recipient=instance.user,
                verb="te ha asignado la jornada de soporte",
                target=instance,
            )


@receiver(post_save, sender=GreenWorkingDay)
def create_or_update_green_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the green working day
    """
    greenworkingday_ct = ContentType.objects.get_for_model(GreenWorkingDay)
    if instance.main_user:
        # Event management
        event_type = EventType.objects.get(pk=EventType.SystemType.GREEN)
        event_obj, event_created = Event.objects.update_or_create(
            link_content_type=greenworkingday_ct,
            link_object_id=instance.id,
            defaults={
                "start_datetime": make_aware(datetime.combine(instance.date, datetime.min.time())),
                "end_datetime": make_aware(datetime.combine(instance.date, datetime.max.time())),
                "all_day": True,
                "type": event_type,
                "name": instance.main_user.acronym,
            },
        )
        attendees = [instance.main_user]
        if instance.support_user:
            attendees.append(instance.support_user)
        event_obj.attendees.set(attendees)

        # Holiday management
        holiday_type = HolidayType.objects.get(pk=HolidayType.SystemType.GREEN)
        if instance.main_user.company and instance.main_user.company.extra_holiday_with_green_working_days:
            holiday_obj, holiday_created = Holiday.objects.update_or_create(
                green_working_day_id=instance.id,
                defaults={"type": holiday_type, "allowance_date": instance.date, "user": instance.main_user},
            )
        else:
            Holiday.objects.filter(green_working_day_id=instance.id).delete()
    else:
        Event.objects.filter(link_content_type=greenworkingday_ct, link_object_id=instance.id).delete()
        Holiday.objects.filter(green_working_day_id=instance.id).delete()


@receiver(pre_save, sender=GreenWorkingDay)
def notify_users_of_existing_green_assignation(sender, instance, *args, **kwargs):
    """
    Notifies users that they have been assigned to an existing Green Working Day
    """
    if instance.persisted and (instance.main_user or instance.support_user):
        old_instance = GreenWorkingDay.objects.get(pk=instance.id)
        notification_sender = instance.notification_sender

        if (
            instance.main_user
            and instance.main_user != notification_sender
            and old_instance.main_user != instance.main_user
        ):
            notify.send(
                sender=notification_sender,
                recipient=instance.main_user,
                verb="te ha asignado, con rol principal, la jornada especial",
                target=instance,
            )
        if (
            instance.support_user
            and instance.support_user != notification_sender
            and old_instance.support_user != instance.support_user
        ):
            notify.send(
                sender=notification_sender,
                recipient=instance.support_user,
                verb="te ha asignado, con rol de soporte, la jornada especial",
                target=instance,
            )


@receiver(post_save, sender=GreenWorkingDay)
def notify_users_of_new_green_assignation(sender, instance, created, *args, **kwargs):
    """
    Notifies users that they have been assigned to an new Green Working Day
    """
    if created and (instance.main_user or instance.support_user):
        notification_sender = instance.notification_sender

        if instance.main_user and instance.main_user != notification_sender:
            notify.send(
                sender=notification_sender,
                recipient=instance.main_user,
                verb="te ha asignado, con rol principal, la jornada especial",
                target=instance,
            )
        if instance.support_user and instance.support_user != notification_sender:
            notify.send(
                sender=notification_sender,
                recipient=instance.support_user,
                verb="te ha asignado, con rol de soporte, la jornada especial",
                target=instance,
            )
