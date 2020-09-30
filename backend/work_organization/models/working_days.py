from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import ModelWithEvent, ModelWithNotifications, UuidModel


class GreenWorkingDay(UuidModel, ModelWithNotifications, ModelWithEvent):
    label = models.CharField(_("etiqueta"), max_length=100, blank=True)
    date = models.DateField(_("fecha"), unique=True, blank=False, null=False)
    main_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario principal"),
        related_name="green_working_days_as_main",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    support_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario de apoyo"),
        related_name="green_working_days_as_support",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    volunteers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuarios voluntarios"),
        related_name="voluntary_green_working_days",
        blank=True,
    )

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name = _("jornada especial")
        verbose_name_plural = _("jornadas especiales")
        ordering = ["-date"]


class SupportWorkingDay(UuidModel, ModelWithNotifications, ModelWithEvent):
    date = models.DateField(_("fecha"), unique=True, blank=False, null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario"),
        related_name="support_working_days",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name = _("jornada de soporte")
        verbose_name_plural = _("jornadas de soporte")
        ordering = ["-date"]
