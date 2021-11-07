from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils.timezone import make_aware

from notifications.signals import notify

from .models import Progress, Sprint, Task, UserStory
from common.utils import notify_item_assignation_to_user
from events.models import Event, EventType


@receiver(post_save, sender=Sprint)
def create_or_update_sprint_calendar_event(sender, instance, created, *args, **kwargs):
    """
    Creates or updates a new system event based on the sprint
    """
    sprint_ct = ContentType.objects.get_for_model(Sprint)
    if instance.end_date:
        event_type = EventType.objects.get(system_slug=EventType.SystemSlug.SPRINT)
        obj, obj_created = Event.objects.update_or_create(
            link_content_type=sprint_ct,
            link_object_id=instance.id,
            defaults={
                "start_datetime": make_aware(datetime.combine(instance.end_date, datetime.min.time())),
                "end_datetime": make_aware(datetime.combine(instance.end_date, datetime.max.time())),
                "all_day": True,
                "type": event_type,
                "name": instance.name,
            },
        )
        obj.attendees.set([instance.accountable_user])
    else:
        Event.objects.filter(link_content_type=sprint_ct, link_object_id=instance.id).delete()


@receiver(pre_save, sender=Sprint)
def notify_users_of_existing_sprint_assignation(sender, instance, *args, **kwargs):
    """
    Notifies an user that has been assigned to an existing Sprint
    """
    if instance.persisted:
        old_instance = Sprint.objects.get(pk=instance.id)
        notify_item_assignation_to_user(
            instance, "accountable_user", "te ha designado como responsable del sprint", old_instance
        )


@receiver(post_save, sender=Sprint)
def notify_users_of_new_sprint_assignation(sender, instance, created, *args, **kwargs):
    """
    Notifies an user that has been assigned to a new Sprint
    """
    if created:
        notify_item_assignation_to_user(instance, "accountable_user", "te ha designado como responsable del sprint")


@receiver(pre_save, sender=UserStory)
def user_story_status_consistency(sender, instance, *args, **kwargs):
    """
    Avoids inconsistent data in 'status', 'validated', 'risk_level' and
    date fields.
    """
    if not instance.sprint_id:
        instance.status = UserStory.Status.BACKLOG
        instance.start_date = None
        instance.end_date = None
    elif instance.current_progress == 0:
        instance.status = UserStory.Status.NOT_STARTED
    elif instance.current_progress > 0 and instance.current_progress < 100:
        instance.status = UserStory.Status.IN_DEVELOPMENT
    elif not instance.validated:
        instance.status = UserStory.Status.IN_VALIDATION
    else:
        instance.status = UserStory.Status.COMPLETED
        instance.risk_level = UserStory.RiskLevel.GREEN

    if instance.current_progress < 100:
        instance.validated = None


@receiver(pre_save, sender=UserStory)
def notify_users_of_existing_user_story_assignation(sender, instance, raw, using, update_fields, *args, **kwargs):
    """
    Notifies users that they have been assigned to an existing User Story
    """
    if not update_fields and instance.persisted:
        old_instance = UserStory.objects.get(pk=instance.id)
        message = "te ha designado como {role} de la historia de usuario"
        development_user = notify_item_assignation_to_user(
            instance, "development_user", message.format(role="desarrollador"), old_instance
        )
        validation_user = notify_item_assignation_to_user(
            instance, "validation_user", message.format(role="validador"), old_instance
        )
        support_user = notify_item_assignation_to_user(
            instance, "support_user", message.format(role="soporte"), old_instance
        )
        instance.change_notification_excluded_users = [development_user, validation_user, support_user]


@receiver(post_save, sender=UserStory)
def notify_users_of_new_user_story_assignation(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """
    Notifies users that they have been assigned to a new User Story
    """
    if created and not update_fields:
        message = "te ha designado como {role} de la historia de usuario"
        notify_item_assignation_to_user(instance, "development_user", message.format(role="desarrollador"))
        notify_item_assignation_to_user(instance, "validation_user", message.format(role="validador"))
        notify_item_assignation_to_user(instance, "support_user", message.format(role="soporte"))


@receiver(post_save, sender=UserStory)
def notify_users_of_user_story_changes(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """
    Notifies assigned users of changes made in an existing User Story
    """
    if not created and not update_fields:
        notification_sender = instance.notification_sender
        excluded_users = instance.change_notification_excluded_users + [notification_sender]
        recipient_qs = (
            get_user_model()
            .objects.active()
            .filter(
                Q(developed_user_stories=instance)
                | Q(validated_user_stories=instance)
                | Q(supported_user_stories=instance)
            )
            .exclude(pk__in=[user.pk for user in excluded_users if user])
            .distinct()
        )

        if recipient_qs.exists():
            notification_verb = "ha modificado la historia de usuario"
            instance.notifications.filter(recipient__in=recipient_qs, verb=notification_verb, unread=True).update(
                unread=False
            )
            notify.send(
                sender=notification_sender,
                recipient=recipient_qs,
                verb=notification_verb,
                target=instance,
            )


@receiver(post_save, sender=Progress)
def update_user_story_current_progress(sender, instance, created, *args, **kwargs):
    """
    Updates user story progress if its current value does not match with the
    last progress log entry.
    """
    last_progress_record = instance.user_story.progress_log.order_by("-date").first()
    if last_progress_record:
        new_progress = last_progress_record.progress
        if new_progress != instance.user_story.current_progress:
            instance.user_story.current_progress = new_progress
            instance.user_story.modification_user = last_progress_record.creation_user
            instance.user_story.save(
                update_fields=[
                    "status",
                    "start_date",
                    "end_date",
                    "risk_level",
                    "validated",
                    "current_progress",
                    "current_progress_changed",
                    "modification_user",
                    "modification_datetime",
                ]
            )


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def calculate_user_story_progress(sender, instance, *args, **kwargs):
    """
    Calculates the new user story progress every time a task is saved or deleted
    """
    task_queryset = Task.objects.filter(user_story_id=instance.user_story_id)
    if task_queryset.exists():
        total_weight_agg = task_queryset.aggregate(total_weight=Coalesce(Sum("weight"), Value(1)))
        done_weight_agg = task_queryset.filter(done=True).aggregate(done_weight=Coalesce(Sum("weight"), Value(0)))
        new_progress = (done_weight_agg["done_weight"] * 100) // total_weight_agg["total_weight"]
    else:
        new_progress = 0
    (progress_record, progress_record_created) = instance.user_story.progress_log.update_or_create(
        date=date.today(), defaults={"progress": new_progress, "creation_user": instance.modification_user}
    )


@receiver(pre_delete, sender=UserStory)
def disconnect_task_signal(sender, instance, *args, **kwargs):
    """
    Disconnects task signal to avoid unnecesary db queries when an user story is
    about to be deleted.
    """
    post_delete.disconnect(receiver=calculate_user_story_progress, sender=Task)


@receiver(post_delete, sender=UserStory)
def reconnect_tasks_signals(sender, instance, *args, **kwargs):
    """
    Reconnects task signal to recover expected behaviour once the user story has
    been deleted.
    """
    post_delete.connect(receiver=calculate_user_story_progress, sender=Task)
