from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .querysets import HolidayQuerySet
from common.behaviors import Eventable, Notifiable, Uuidable


class GreenWorkingDay(Uuidable, Notifiable, Eventable, models.Model):
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


class SupportWorkingDay(Uuidable, Notifiable, Eventable, models.Model):
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


class HolidayType(models.Model):
    class SystemSlug(models.TextChoices):
        GENERAL = "GENERAL", _("General")
        GREEN = "GREEN", _("Jornada especial")

    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)
    validity = models.DurationField(
        _("período de validez"),
        help_text=_("Período de validez desde la fecha de concesión. Formato: '[DIAS] [HORAS]:[MINUTOS]:[SEGUNDOS]'"),
        blank=False,
        null=False,
    )
    system_slug = models.CharField(
        _("slug de sistema"),
        choices=SystemSlug.choices,
        max_length=20,
        blank=True,
        null=True,
        default=None,
        editable=False,
        db_index=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("tipo de vacaciones")
        verbose_name_plural = _("tipos de vacaciones")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["system_slug"], condition=Q(system_slug__isnull=False), name="unique_holiday_type_slug"
            )
        ]


def holiday_type_default():
    try:
        general_type = HolidayType.objects.get(system_slug=HolidayType.SystemSlug.GENERAL)
        return general_type.pk
    except HolidayType.DoesNotExist:
        return None


class Holiday(Uuidable, Notifiable, Eventable, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario"),
        related_name="holidays",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        HolidayType,
        verbose_name=_("tipo"),
        related_name="holidays",
        blank=False,
        null=False,
        default=holiday_type_default,
        on_delete=models.PROTECT,
    )
    allowance_date = models.DateField(_("fecha de concesión"), blank=False, null=False, default=date.today)
    planned_date = models.DateField(_("fecha planificada"), blank=True, null=True)
    approved = models.BooleanField(_("aprobado"), null=True, blank=True)
    green_working_day = models.OneToOneField(
        GreenWorkingDay,
        verbose_name=_("jornada especial"),
        related_name="holiday",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def expiration_date(self):
        return self.allowance_date + self.type.validity

    @property
    def notification_str(self):
        return f"{self.planned_date}"

    objects = HolidayQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.user} ({self.allowance_date.year})"

    class Meta:
        verbose_name = _("día de vacaciones")
        verbose_name_plural = _("días de vacaciones")
        ordering = ["-planned_date", "user"]
