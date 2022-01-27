import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GreenWorkingDay",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("label", models.CharField(blank=False, max_length=100, verbose_name="etiqueta")),
                ("date", models.DateField(unique=True, verbose_name="fecha")),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_greenworkingday_creations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de creación",
                    ),
                ),
                (
                    "main_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="green_working_days_as_main",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario principal",
                    ),
                ),
                (
                    "modification_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_greenworkingday_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "support_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="green_working_days_as_support",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de apoyo",
                    ),
                ),
                (
                    "volunteers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="voluntary_green_working_days",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuarios voluntarios",
                    ),
                ),
            ],
            options={
                "verbose_name": "jornada especial",
                "verbose_name_plural": "jornadas especiales",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="HolidayType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
                (
                    "validity",
                    models.DurationField(
                        help_text="Período de validez desde la fecha de concesión. Formato: '[DIAS] [HORAS]:[MINUTOS]:[SEGUNDOS]'",
                        verbose_name="período de validez",
                    ),
                ),
                (
                    "system",
                    models.BooleanField(
                        default=False,
                        editable=False,
                        help_text="Los tipos de sistema no pueden/deben ser modificados ni eliminados",
                        verbose_name="de sistema",
                    ),
                ),
            ],
            options={
                "verbose_name": "tipo de vacaciones",
                "verbose_name_plural": "tipos de vacaciones",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SupportWorkingDay",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField(unique=True, verbose_name="fecha")),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_supportworkingday_creations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de creación",
                    ),
                ),
                (
                    "modification_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_supportworkingday_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="support_working_days",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "jornada de soporte",
                "verbose_name_plural": "jornadas de soporte",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Holiday",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("allowance_date", models.DateField(default=datetime.date.today, verbose_name="fecha de concesión")),
                ("planned_date", models.DateField(blank=True, null=True, verbose_name="fecha planificada")),
                ("approved", models.BooleanField(blank=True, null=True, verbose_name="aprobado")),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_holiday_creations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de creación",
                    ),
                ),
                (
                    "green_working_day",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="holiday",
                        to="work_organization.GreenWorkingDay",
                        verbose_name="jornada especial",
                    ),
                ),
                (
                    "modification_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="work_organization_holiday_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="holidays",
                        to="work_organization.HolidayType",
                        verbose_name="tipo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="holidays",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "día de vacaciones",
                "verbose_name_plural": "días de vacaciones",
                "ordering": ["-planned_date", "user"],
            },
        ),
    ]
