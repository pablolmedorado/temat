import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class Uuidable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def persisted(self):
        return self.__class__.objects.filter(id=self.id).exists()

    class Meta:
        abstract = True


class Authorable(models.Model):
    OWNERSHIP_FIELD = "creation_user"

    creation_datetime = models.DateTimeField(
        _("fecha de creación"), auto_now_add=True, blank=False, null=False, editable=False
    )
    modification_datetime = models.DateTimeField(
        _("fecha de modificación"), auto_now=True, blank=False, null=False, editable=False
    )

    creation_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name=_("usuario de creación"),
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_creations",
    )
    modification_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name=_("usuario de modificación"),
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_modifications",
    )

    class Meta:
        abstract = True


class Eventable(models.Model):
    events = GenericRelation(
        "events.Event",
        content_type_field="link_content_type",
        object_id_field="link_object_id",
        related_query_name="%(app_label)s_%(class)s",
    )

    class Meta:
        abstract = True


class Notifiable(Authorable):
    notifications = GenericRelation(
        "notifications.Notification",
        content_type_field="target_content_type",
        object_id_field="target_object_id",
        related_query_name="%(app_label)s_%(class)s",
    )

    @property
    def notification_str(self):
        return f"{self}"

    @property
    def notification_sender(self):
        return (
            self.modification_user or self.creation_user or get_user_model().objects.filter(is_superuser=True).first()
        )

    class Meta:
        abstract = True


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Taggable(Uuidable):
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)

    class Meta:
        abstract = True
