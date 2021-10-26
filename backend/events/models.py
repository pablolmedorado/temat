import operator
from functools import reduce
from typing import List

import django.utils.timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from icalendar import Calendar, Event as ICalendarEvent, vCalAddress, vText

from .querysets import EventQuerySet
from common.behaviors import Notifiable, Taggable


class EventType(models.Model):
    class SystemSlug(models.TextChoices):
        HOLIDAY = "HOLIDAY", _("Vacaciones")
        SUPPORT = "SUPPORT", _("Soporte")
        GREEN = "GREEN", _("Jornada especial")
        SPRINT = "SPRINT", _("Sprint")

    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)
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
    colour = ColorField(_("color en la aplicación"), blank=True, default="#737373")
    icon = models.CharField(
        _("icono en la aplicación"),
        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
        max_length=50,
        blank=True,
    )
    important = models.BooleanField(
        _("importante"), help_text=_("Mostrar fechas de eventos de este tipo en selectores de fecha"), default=False
    )

    def __str__(self):
        return self.name

    def colored_colour(self):
        return format_html('<span style="color: {colour};">{colour}</span>', colour=self.colour)

    colored_colour.short_description = _("Color")  # type: ignore
    colored_colour.admin_order_field = "colour"  # type: ignore

    class Meta:
        verbose_name = _("tipo de evento")
        verbose_name_plural = _("tipos de evento")
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["system_slug"], condition=Q(system_slug__isnull=False), name="unique_event_type_slug"
            )
        ]


class Event(Taggable, Notifiable, models.Model):
    ALLOWED_LINK_TYPES = (
        ("work_organization", "holiday"),
        ("work_organization", "greenworkingday"),
        ("work_organization", "supportworkingday"),
        ("scrum", "sprint"),
    )
    ALLOWED_LINK_TYPES_Q = reduce(
        operator.or_, [Q(**{"app_label": app, "model": model}) for app, model in ALLOWED_LINK_TYPES]
    )

    class VisibilityType(models.TextChoices):
        PUBLIC = "PU", _("Público")
        PRIVATE = "PR", _("Privado")

    name = models.CharField(_("nombre"), max_length=200, blank=False)
    type = models.ForeignKey(
        EventType, verbose_name=_("tipo"), related_name="events", blank=False, null=False, on_delete=models.PROTECT
    )
    details = models.CharField(_("detalles"), max_length=2000, blank=True)
    start_datetime = models.DateTimeField(_("inicio"), blank=False, null=False, default=django.utils.timezone.now)
    end_datetime = models.DateTimeField(_("fin"), blank=False, null=False, default=django.utils.timezone.now)
    all_day = models.BooleanField(_("todo el día"), default=True)
    visibility = models.CharField(
        _("visibilidad"),
        help_text=_("Visibilidad del evento. Privado implica que sólo los invitados pueden verlo/acceder."),
        choices=VisibilityType.choices,
        default=VisibilityType.PUBLIC,
        max_length=2,
        db_index=True,
    )
    location = models.CharField(_("ubicación"), max_length=200, blank=True)
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("usuarios invitados"), related_name="events", blank=True
    )
    groups = models.ManyToManyField(Group, verbose_name=_("grupos invitados"), related_name="events", blank=True)

    # Link
    link_content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("tipo del enlace"),
        help_text=_("Tipo de objeto de sistema al que está enlazado este evento."),
        blank=True,
        null=True,
        limit_choices_to=ALLOWED_LINK_TYPES_Q,
        on_delete=models.CASCADE,
    )
    link_object_id = models.UUIDField(
        _("id del objeto enlazado"),
        help_text=_("Identificador del objeto de sistema al que está enlazado este evento."),
        blank=True,
        null=True,
    )
    link = GenericForeignKey("link_content_type", "link_object_id")

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    def to_icalendar_event(self) -> ICalendarEvent:
        ical_event = ICalendarEvent()

        ical_event["uid"] = self.id
        ical_event.add("summary", self.name if not self.type.system_slug else f"[{self.type.name}] {self.name}")
        ical_event.add("description", self.details)
        ical_event.add("location", self.location)
        ical_event.add("dtstart", self.start_datetime)
        ical_event.add("dtend", self.end_datetime)
        ical_event.add("categories", [self.type.name])
        ical_event.add("dtstamp", self.creation_datetime)

        if self.creation_user:
            organizer = vCalAddress(f"MAILTO:{self.creation_user.email}")
            organizer.params["cn"] = vText(self.creation_user.get_full_name())
            organizer.params["role"] = vText("CHAIR")
            ical_event["organizer"] = organizer

        attendees_list = get_user_model().objects.active().filter(Q(events=self) | Q(groups__events=self)).distinct()
        for user in attendees_list:
            if user.email:
                attendee = vCalAddress(f"MAILTO:{user.email}")
                attendee.params["cn"] = vText(user.get_full_name())
                attendee.params["ROLE"] = vText("REQ-PARTICIPANT")
                ical_event.add("attendee", attendee, encode=0)

        return ical_event

    @staticmethod
    def from_list_to_icalendar(event_list: List) -> Calendar:
        ical = Calendar()
        for event in event_list:
            ical.add_component(event.to_icalendar_event())
        return ical

    class Meta:
        verbose_name = _("evento")
        verbose_name_plural = _("eventos")
        ordering = ("-start_datetime",)
