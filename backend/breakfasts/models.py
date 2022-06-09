from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.behaviors import Transactionable


class Bread(Transactionable, models.Model):
    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = _("pan")
        verbose_name_plural = _("panes")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Base(Transactionable, models.Model):
    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = _("base")
        verbose_name_plural = _("bases")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Ingredient(Transactionable, models.Model):
    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = _("ingrediente")
        verbose_name_plural = _("ingredientes")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Drink(Transactionable, models.Model):
    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = _("bebida")
        verbose_name_plural = _("bebidas")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Breakfast(Transactionable, models.Model):
    OWNERSHIP_FIELD = "user"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario"),
        related_name="breakfasts",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    bread = models.ForeignKey(
        Bread, verbose_name=_("pan"), related_name="breakfasts", blank=False, null=False, on_delete=models.PROTECT
    )
    base = models.ForeignKey(
        Base, verbose_name=_("base"), related_name="breakfasts", blank=False, null=False, on_delete=models.PROTECT
    )
    ingredient1 = models.ForeignKey(
        Ingredient,
        verbose_name=_("primer ingrediente"),
        related_name="breakfasts_as_first_ingredient",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    ingredient2 = models.ForeignKey(
        Ingredient,
        verbose_name=_("segundo ingrediente"),
        related_name="breakfasts_as_second_ingredient",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    drink = models.ForeignKey(
        Drink, verbose_name=_("bebida"), related_name="breakfasts", blank=True, null=True, on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("desayuno")
        verbose_name_plural = _("desayunos")
        ordering = ("user",)

    def __str__(self):
        return f"{self.user}"
