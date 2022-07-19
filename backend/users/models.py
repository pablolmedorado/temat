from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.behaviors import Transactionable
from common.decorators import atomic_transaction_singleton
from .managers import UserManager


class Company(Transactionable, models.Model):
    name = models.CharField(_("nombre"), max_length=200, blank=False, unique=True)
    yearly_holiday_allocation = models.PositiveSmallIntegerField(
        _("días de vacaciones al año"),
        help_text=_("Número de días de vacaciones que la empresa da a sus empleados anualmente"),
        blank=False,
        null=False,
    )
    extra_holiday_with_green_working_days = models.BooleanField(_("vacaciones extra con dias verdes"), default=True)

    class Meta:
        verbose_name = _("empresa")
        verbose_name_plural = _("empresas")
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(Transactionable, AbstractUser):
    REQUIRED_FIELDS = ["first_name", "last_name", "acronym"]

    acronym = models.CharField(
        _("siglas"),
        help_text=_("Siglas identificativas del usuario para vistas resumen. Máximo 3 caracteres."),
        max_length=3,
        blank=False,
    )
    company = models.ForeignKey(
        Company,
        verbose_name=_("empresa"),
        help_text=_("Empresa para la que trabaja el usuario"),
        related_name="employees",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["first_name", "last_name", "acronym"]

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return super().__str__()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return f"{self.acronym}"

    @atomic_transaction_singleton
    def assign_year_holidays(self, year=None):
        if self.company and self.is_active:
            holidays_year = year if year else date.today().year
            holidays_allowance_date = date(holidays_year, 1, 1)

            for number in range(self.company.yearly_holiday_allocation):
                self.holidays.create(allowance_date=holidays_allowance_date)
