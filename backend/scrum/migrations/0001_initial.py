import colorfield.fields
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Epic",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="nombre")),
                ("description", models.CharField(blank=True, max_length=2000, verbose_name="descripción")),
                (
                    "external_reference",
                    models.CharField(blank=True, max_length=2000, verbose_name="referencia externa"),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_epic_creations",
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
                        related_name="scrum_epic_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
            ],
            options={"verbose_name": "epic", "verbose_name_plural": "epics", "ordering": ("-creation_datetime",)},
        ),
        migrations.CreateModel(
            name="Sprint",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="nombre")),
                ("start_date", models.DateField(default=datetime.date.today, verbose_name="fecha de inicio")),
                ("end_date", models.DateField(verbose_name="fecha de fin")),
                (
                    "accountable_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sprints_as_accountable",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="responsable",
                    ),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_sprint_creations",
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
                        related_name="scrum_sprint_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
            ],
            options={"verbose_name": "sprint", "verbose_name_plural": "sprints", "ordering": ("-start_date",)},
        ),
        migrations.CreateModel(
            name="UserStoryType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
                (
                    "colour",
                    colorfield.fields.ColorField(
                        default="#FFFFFF", max_length=18, verbose_name="color en las gráficas"
                    ),
                ),
            ],
            options={
                "verbose_name": "tipo de historia de usuario",
                "verbose_name_plural": "tipos de historia de usuario",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="UserStory",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=500, verbose_name="nombre")),
                (
                    "functional_description",
                    models.CharField(blank=True, max_length=2000, verbose_name="descripción técnica"),
                ),
                (
                    "technical_description",
                    models.CharField(blank=True, max_length=2000, verbose_name="descripción funcional"),
                ),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="fecha de inicio")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="fecha límite")),
                (
                    "current_progress",
                    models.PositiveSmallIntegerField(
                        default=0,
                        editable=False,
                        validators=[django.core.validators.MaxValueValidator(100)],
                        verbose_name="avance actual",
                    ),
                ),
                (
                    "current_progress_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now,
                        editable=False,
                        monitor="current_progress",
                        verbose_name="último cambio de avance",
                    ),
                ),
                ("validated", models.BooleanField(blank=True, null=True, verbose_name="validada")),
                (
                    "validated_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now,
                        editable=False,
                        monitor="validated",
                        verbose_name="último cambio en validación",
                    ),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Backlog"),
                            (1, "Sin comenzar"),
                            (2, "En desarrollo"),
                            (3, "En validación"),
                            (4, "Completada"),
                        ],
                        db_index=True,
                        default=0,
                        editable=False,
                        verbose_name="estado",
                    ),
                ),
                (
                    "planned_effort",
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text="Calculado en 'unidades de trabajo'. 1UT = 1/2h.",
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="esfuerzo planificado",
                    ),
                ),
                (
                    "priority",
                    models.PositiveSmallIntegerField(
                        default=10,
                        help_text="A menor número, mayor importancia",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name="prioridad",
                    ),
                ),
                (
                    "development_comments",
                    models.CharField(blank=True, max_length=2000, verbose_name="comentarios de desarrollo"),
                ),
                (
                    "validation_comments",
                    models.CharField(blank=True, max_length=2000, verbose_name="comentarios de validación"),
                ),
                (
                    "support_comments",
                    models.CharField(blank=True, max_length=2000, verbose_name="comentarios de soporte"),
                ),
                (
                    "cvs_reference",
                    models.CharField(
                        blank=True, help_text="Rama de git.", max_length=255, verbose_name="referencia scv"
                    ),
                ),
                (
                    "risk_level",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Verde"), (1, "Naranja"), (2, "Rojo")], default=0, verbose_name="nivel de riesgo"
                    ),
                ),
                ("risk_comments", models.CharField(blank=True, max_length=2000, verbose_name="comentarios de riesgo")),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_userstory_creations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de creación",
                    ),
                ),
                (
                    "development_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="developed_user_stories",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="desarrollador",
                    ),
                ),
                (
                    "epic",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_stories",
                        to="scrum.Epic",
                        verbose_name="epic",
                    ),
                ),
                (
                    "modification_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_userstory_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "sprint",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_stories",
                        to="scrum.Sprint",
                        verbose_name="sprint",
                    ),
                ),
                (
                    "support_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="supported_user_stories",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="soporte",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user_stories",
                        to="scrum.UserStoryType",
                        verbose_name="tipo",
                    ),
                ),
                (
                    "validation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="validated_user_stories",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="validador",
                    ),
                ),
            ],
            options={
                "verbose_name": "historia de usuario",
                "verbose_name_plural": "historias de usuario",
                "ordering": ("-start_date",),
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("order", models.PositiveIntegerField(db_index=True, editable=False, verbose_name="order")),
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=2000, verbose_name="nombre")),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name="peso"
                    ),
                ),
                ("done", models.BooleanField(default=False, verbose_name="finalizada")),
                (
                    "done_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now,
                        editable=False,
                        monitor="done",
                        verbose_name="último cambio en finalizada",
                    ),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_task_creations",
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
                        related_name="scrum_task_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "user_story",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="scrum.UserStory",
                        verbose_name="historia de usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "tarea",
                "verbose_name_plural": "tareas",
                "ordering": ("order",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Progress",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField(default=datetime.date.today, verbose_name="fecha")),
                (
                    "progress",
                    models.PositiveSmallIntegerField(
                        default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name="avance"
                    ),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_progress_creations",
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
                        related_name="scrum_progress_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "user_story",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="progress_log",
                        to="scrum.UserStory",
                        verbose_name="historia de usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "registro de avance",
                "verbose_name_plural": "histórico de avance",
                "ordering": ("-date",),
            },
        ),
        migrations.CreateModel(
            name="Effort",
            fields=[
                ("creation_datetime", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("modification_datetime", models.DateTimeField(auto_now=True, verbose_name="fecha de modificación")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField(default=datetime.date.today, verbose_name="fecha")),
                (
                    "role",
                    models.CharField(
                        choices=[("D", "Desarrollo"), ("V", "Validación"), ("S", "Soporte")],
                        db_index=True,
                        max_length=1,
                        verbose_name="rol",
                    ),
                ),
                (
                    "effort",
                    models.PositiveSmallIntegerField(
                        help_text="Calculado en 'unidades de trabajo'. 1UT = 1/2h.",
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="esfuerzo",
                    ),
                ),
                ("comments", models.CharField(blank=True, max_length=2000, verbose_name="comentarios")),
                (
                    "creation_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="scrum_effort_creations",
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
                        related_name="scrum_effort_modifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario de modificación",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="effort_allocation",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario",
                    ),
                ),
                (
                    "user_story",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="effort_allocation",
                        to="scrum.UserStory",
                        verbose_name="historia de usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "asignación de esfuerzo",
                "verbose_name_plural": "asignaciones de esfuerzo",
                "ordering": ("-creation_datetime",),
            },
        ),
        migrations.AddConstraint(
            model_name="userstory",
            constraint=models.UniqueConstraint(fields=("name", "sprint"), name="unique_user_story_sprint"),
        ),
        migrations.AddConstraint(
            model_name="userstory",
            constraint=models.UniqueConstraint(fields=("name", "epic"), name="unique_user_story_epic"),
        ),
        migrations.AddConstraint(
            model_name="task", constraint=models.UniqueConstraint(fields=("name", "user_story"), name="unique_task")
        ),
        migrations.AddConstraint(
            model_name="progress",
            constraint=models.UniqueConstraint(fields=("date", "user_story"), name="unique_progress"),
        ),
        migrations.AddConstraint(
            model_name="effort",
            constraint=models.UniqueConstraint(fields=("date", "user", "role", "user_story"), name="unique_effort"),
        ),
    ]
