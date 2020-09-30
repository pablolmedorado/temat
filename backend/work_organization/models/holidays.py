from datetime import date

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..querysets import HolidayQuerySet
from .working_days import GreenWorkingDay
from common.models import ModelWithEvent, ModelWithNotifications, UuidModel


class HolidayType(models.Model):
    class SystemType(models.IntegerChoices):
        GENERAL = 1, _("General")
        GREEN = 2, _("Jornada especial")

    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)
    validity = models.DurationField(
        _("período de validez"),
        help_text=_("Período de validez desde la fecha de concesión. Formato: '[DIAS] [HORAS]:[MINUTOS]:[SEGUNDOS]'"),
        blank=False,
        null=False,
    )
    system = models.BooleanField(
        _("de sistema"),
        help_text=_("Los tipos de sistema no pueden/deben ser modificados ni eliminados"),
        default=False,
        editable=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("tipo de vacaciones")
        verbose_name_plural = _("tipos de vacaciones")
        ordering = ["name"]


class Holiday(UuidModel, ModelWithNotifications, ModelWithEvent):
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
        default=HolidayType.SystemType.GENERAL,
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
