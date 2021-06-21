from django.db import models
from django.utils.translation import ugettext_lazy as _

from ordered_model.models import OrderedModel as Orderable


class LinkType(Orderable, models.Model):
    name = models.CharField(_("nombre"), max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(Orderable.Meta):
        verbose_name = _("tipo de enlace")
        verbose_name_plural = _("tipos de enlace")


class Link(Orderable, models.Model):
    name = models.CharField(_("nombre"), max_length=2000, blank=False, unique=True)
    icon = models.CharField(
        _("icono en la aplicación"),
        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
        max_length=50,
        blank=False,
    )
    url = models.URLField(_("url"), max_length=2000, blank=False, unique=True)
    type = models.ForeignKey(
        LinkType, verbose_name=_("tipo"), related_name="links", blank=False, null=False, on_delete=models.PROTECT,
    )

    order_with_respect_to = ("type",)

    def __str__(self):
        return self.name

    class Meta(Orderable.Meta):
        verbose_name = _("enlace")
        verbose_name_plural = _("enlaces")
