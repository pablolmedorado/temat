from typing import Any, Optional

from notifications.signals import notify


def notify_item_assignation_to_user(
    new_instance: Any, user_field: str, message: str, old_instance: Any = None
) -> Optional[Any]:
    new_user = getattr(new_instance, user_field)
    old_user = getattr(old_instance, user_field) if old_instance else None
    notification_sender = new_instance.notification_sender

    if new_user and new_user != notification_sender and old_user != new_user:
        notify.send(
            sender=notification_sender, recipient=new_user, verb=message, target=new_instance,
        )
        return new_user
    return None
