from typing import Any, Optional, TYPE_CHECKING

from django.contrib.auth import get_user_model

from django_currentuser.middleware import get_current_authenticated_user
from notifications.signals import notify

if TYPE_CHECKING:
    from users.models import User


def get_notification_sender() -> "User":
    return get_current_authenticated_user() or get_user_model().objects.get_random_admin()


def notify_item_assignation_to_user(
    new_instance: Any, user_field: str, message: str, old_instance: Any = None
) -> Optional[Any]:
    new_user = getattr(new_instance, user_field)
    old_user = getattr(old_instance, user_field) if old_instance else None
    notification_sender = get_notification_sender()

    if new_user and new_user != notification_sender and old_user != new_user:
        notify.send(sender=notification_sender, recipient=new_user, verb=message, target=new_instance)
        return new_user
    return None
