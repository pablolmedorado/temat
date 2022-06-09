import uuid

import colorfield.fields

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0011_update_proxy_permissions"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("work_organization", "0001_initial"),
        ("scrum", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
                (
                    "colour",
                    colorfield.fields.ColorField(
                        blank=True, default="#737373", max_length=18, verbose_name="color en la aplicación"
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
                        max_length=50,
                        verbose_name="icono en la aplicación",
                    ),
                ),
                (
                    "important",
                    models.BooleanField(
                        default=False,
                        help_text="Mostrar fechas de eventos de este tipo en selectores de fecha",
                        verbose_name="importante",
                    ),
                ),
                (
                    "system",
                    models.BooleanField(
                        default=False,
                        editable=False,
                        help_text="Los eventos de sistema no pueden/deben ser modificados ni eliminados",
                        verbose_name="de sistema",
                    ),
                ),
            ],
            options={
                "verbose_name": "tipo de evento",
                "verbose_name_plural": "tipos de evento",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, verbose_name="nombre")),
                ("details", models.CharField(blank=True, max_length=2000, verbose_name="detalles")),
                ("start_datetime", models.DateTimeField(default=django.utils.timezone.now, verbose_name="inicio")),
                ("end_datetime", models.DateTimeField(default=django.utils.timezone.now, verbose_name="fin")),
                ("all_day", models.BooleanField(default=True, verbose_name="todo el día")),
                (
                    "visibility",
                    models.CharField(
                        choices=[("PU", "Público"), ("PR", "Privado")],
                        db_index=True,
                        default="PU",
                        help_text="Visibilidad del evento. Privado implica que sólo los invitados pueden verlo/acceder.",
                        max_length=2,
                        verbose_name="visibilidad",
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=200, verbose_name="ubicación")),
                (
                    "link_object_id",
                    models.UUIDField(
                        blank=True,
                        help_text="Identificador del objeto de sistema al que está enlazado este evento.",
                        null=True,
                        verbose_name="id del objeto enlazado",
                    ),
                ),
                (
                    "attendees",
                    models.ManyToManyField(
                        blank=True,
                        related_name="events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuarios invitados",
                    ),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="events_event_creations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de creación",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="events", to="auth.Group", verbose_name="grupos invitados"
                    ),
                ),
                (
                    "link_content_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Tipo de objeto de sistema al que está enlazado este evento.",
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "work_organization"), ("model", "holiday")),
                            models.Q(("app_label", "work_organization"), ("model", "greenworkingday")),
                            models.Q(("app_label", "work_organization"), ("model", "supportworkingday")),
                            models.Q(("app_label", "scrum"), ("model", "sprint")),
                            _connector="OR",
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                        verbose_name="tipo del enlace",
                    ),
                ),
                (
                    "modification_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="events_event_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="events",
                        to="events.EventType",
                        verbose_name="tipo",
                    ),
                ),
            ],
            options={"verbose_name": "evento", "verbose_name_plural": "eventos", "ordering": ("-start_datetime",)},
        ),
    ]
