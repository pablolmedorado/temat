from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from ordered_model.models import OrderedModel as Orderable
from taggit.models import GenericUUIDTaggedItemBase, TagBase

from .behaviors import Transactionable


class Tag(Transactionable, TagBase):
    colour = ColorField(_("color en la aplicación"), blank=True, default="#00AEC7")
    icon = models.CharField(
        _("icono en la aplicación"),
        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
        max_length=50,
        blank=True,
        default="mdi-label",
    )

    def colored_colour(self):
        return format_html('<span style="color: {colour};">{colour}</span>', colour=self.colour)

    colored_colour.short_description = _("Color")  # type: ignore
    colored_colour.admin_order_field = "colour"  # type: ignore

    class Meta:
        verbose_name = _("etiqueta")
        verbose_name_plural = _("etiquetas")


class TaggedItem(Transactionable, GenericUUIDTaggedItemBase):
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ítem etiquetado")
        verbose_name_plural = _("ítems etiquetados")
        index_together = [["content_type", "object_id"]]
        unique_together = [["content_type", "object_id", "tag"]]


class LinkType(Transactionable, Orderable, models.Model):
    name = models.CharField(_("nombre"), max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(Orderable.Meta):
        verbose_name = _("tipo de enlace")
        verbose_name_plural = _("tipos de enlace")


class Link(Transactionable, Orderable, models.Model):
    name = models.CharField(_("nombre"), max_length=2000, blank=False, unique=True)
    icon = models.CharField(
        _("icono en la aplicación"),
        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
        max_length=50,
        blank=False,
    )
    url = models.URLField(_("url"), max_length=2000, blank=False, unique=True)
    type = models.ForeignKey(
        LinkType,
        verbose_name=_("tipo"),
        related_name="links",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    order_with_respect_to = ("type",)

    def __str__(self):
        return self.name

    class Meta(Orderable.Meta):
        verbose_name = _("enlace")
        verbose_name_plural = _("enlaces")
