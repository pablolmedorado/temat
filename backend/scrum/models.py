from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.db import models, transaction
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from model_utils.fields import MonitorField
from ordered_model.models import OrderedModel as Orderable

from .behaviors import UserStoryContainer
from .querysets import EpicQuerySet, SprintQuerySet, UserStoryQuerySet
from common.behaviors import Authorable, Eventable, Notifiable, Taggable, Uuidable


class Sprint(Taggable, Notifiable, Eventable, UserStoryContainer, models.Model):
    name = models.CharField(_("nombre"), max_length=200, blank=False, unique=True)
    start_date = models.DateField(_("fecha de inicio"), blank=False, null=False, default=date.today)
    end_date = models.DateField(_("fecha de fin"), blank=False, null=False)
    accountable_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("responsable"),
        related_name="sprints_as_accountable",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    @property
    def ongoing(self):
        if hasattr(self, "annotated_ongoing"):
            return self.annotated_ongoing
        return self.start_date <= date.today() and self.end_date >= date.today()

    objects = SprintQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("sprint")
        verbose_name_plural = _("sprints")
        ordering = ("-start_date",)


class Epic(Taggable, Authorable, UserStoryContainer, models.Model):
    name = models.CharField(_("nombre"), max_length=200, blank=False, unique=True)
    description = models.CharField(_("descripción"), max_length=2000, blank=True)
    external_reference = models.CharField(_("referencia externa"), max_length=2000, blank=True)

    objects = EpicQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("epic")
        verbose_name_plural = _("epics")
        ordering = ("-creation_datetime",)


class UserStoryType(models.Model):
    name = models.CharField(_("nombre"), max_length=50, blank=False, unique=True)
    colour = ColorField(_("color en las gráficas"), blank=False)

    def __str__(self):
        return self.name

    def colored_colour(self):
        return format_html('<span style="color: {colour};">{colour}</span>', colour=self.colour)

    colored_colour.short_description = _("Color")  # type: ignore
    colored_colour.admin_order_field = "colour"  # type: ignore

    class Meta:
        verbose_name = _("tipo de historia de usuario")
        verbose_name_plural = _("tipos de historia de usuario")
        ordering = ("name",)


class UserStory(Taggable, Notifiable, models.Model):
    class Status(models.IntegerChoices):
        BACKLOG = 0, _("Backlog")
        NOT_STARTED = 1, _("Sin comenzar")
        IN_DEVELOPMENT = 2, _("En desarrollo")
        IN_VALIDATION = 3, _("En validación")
        COMPLETED = 4, _("Completada")

    class RiskLevel(models.IntegerChoices):
        GREEN = 0, _("Verde")
        ORANGE = 1, _("Naranja")
        RED = 2, _("Rojo")

    name = models.CharField(_("nombre"), max_length=500, blank=False)
    type = models.ForeignKey(
        UserStoryType,
        verbose_name=_("tipo"),
        related_name="user_stories",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    epic = models.ForeignKey(
        Epic, verbose_name=_("epic"), related_name="user_stories", blank=True, null=True, on_delete=models.CASCADE
    )
    sprint = models.ForeignKey(
        Sprint, verbose_name=_("sprint"), related_name="user_stories", blank=True, null=True, on_delete=models.CASCADE
    )
    functional_description = models.CharField(_("descripción técnica"), max_length=2000, blank=True)
    technical_description = models.CharField(_("descripción funcional"), max_length=2000, blank=True)
    external_resource = models.CharField(
        _("recurso externo"),
        help_text="Ruta a un fichero o directorio con recursos externos",
        max_length=2000,
        blank=True,
        validators=[URLValidator(schemes=["http", "https", "file", "ftp", "ftps"])],
    )
    start_date = models.DateField(_("fecha de inicio"), blank=True, null=True)
    end_date = models.DateField(_("fecha límite"), blank=True, null=True)
    current_progress = models.PositiveSmallIntegerField(
        _("avance actual"), blank=False, default=0, validators=[MaxValueValidator(100)], editable=False
    )
    current_progress_changed = MonitorField(_("último cambio de avance"), monitor="current_progress")
    validated = models.BooleanField(_("validada"), null=True, blank=True)
    validated_changed = MonitorField(_("último cambio en validación"), monitor="validated")
    status = models.PositiveSmallIntegerField(
        _("estado"), choices=Status.choices, default=Status.BACKLOG, blank=False, editable=False, db_index=True,
    )
    planned_effort = models.PositiveSmallIntegerField(
        _("esfuerzo planificado"),
        help_text="Calculado en 'unidades de trabajo'. 1UT = 1/2h.",
        blank=False,
        default=1,
        validators=[MinValueValidator(1)],
    )
    priority = models.PositiveSmallIntegerField(
        _("prioridad"),
        help_text="A menor número, mayor importancia",
        blank=False,
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    development_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("desarrollador"),
        related_name="developed_user_stories",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    development_comments = models.CharField(_("comentarios de desarrollo"), max_length=2000, blank=True)
    validation_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("validador"),
        related_name="validated_user_stories",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    validation_comments = models.CharField(_("comentarios de validación"), max_length=2000, blank=True)
    support_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("soporte"),
        related_name="supported_user_stories",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    support_comments = models.CharField(_("comentarios de soporte"), max_length=2000, blank=True)
    cvs_reference = models.CharField(_("referencia scv"), help_text="Rama de git.", max_length=255, blank=True)
    risk_level = models.PositiveSmallIntegerField(
        _("nivel de riesgo"), choices=RiskLevel.choices, default=RiskLevel.GREEN, blank=False
    )
    risk_comments = models.CharField(_("comentarios de riesgo"), max_length=2000, blank=True)
    use_migrations = models.BooleanField(_("usa migraciones"), default=False)
    deployment_notes = models.CharField(_("notas de despliegue"), max_length=2000, blank=True)

    @property
    def actual_effort(self):
        if hasattr(self, "annotated_actual_effort"):
            return self.annotated_actual_effort
        actual_effort = self.effort_allocation.all().aggregate(effort__sum=Coalesce(Sum("effort"), Value(0)))
        return actual_effort["effort__sum"]

    objects = UserStoryQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    @classmethod
    @transaction.atomic
    def get_copy(cls, instance, owner=None):
        new_instance = cls.objects.create(
            **{
                "name": f"{instance.name} (copia)",
                "type": instance.type,
                "functional_description": instance.functional_description,
                "technical_description": instance.technical_description,
                "planned_effort": instance.planned_effort,
                "priority": instance.priority,
                "use_migrations": instance.use_migrations,
                "creation_user": owner if owner else instance.creation_user,
            }
        )
        # Tasks
        for task in instance.tasks.all().iterator():
            new_instance.tasks.create(**{"name": task.name, "weight": task.weight})
        return new_instance

    class Meta:
        verbose_name = _("historia de usuario")
        verbose_name_plural = _("historias de usuario")
        ordering = ("-start_date",)
        constraints = [
            models.UniqueConstraint(fields=["name", "sprint"], name="unique_user_story_sprint"),
            models.UniqueConstraint(fields=["name", "epic"], name="unique_user_story_epic"),
        ]


class Progress(Uuidable, Authorable, models.Model):
    user_story = models.ForeignKey(
        UserStory,
        verbose_name=_("historia de usuario"),
        related_name="progress_log",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    date = models.DateField(_("fecha"), blank=False, null=False, default=date.today)
    progress = models.PositiveSmallIntegerField(
        _("avance"), blank=False, default=0, validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.date} / {self.user_story} / {self.progress}"

    class Meta:
        verbose_name = _("registro de avance")
        verbose_name_plural = _("histórico de avance")
        ordering = ("-date",)
        constraints = [models.UniqueConstraint(fields=["date", "user_story"], name="unique_progress")]


class Effort(Uuidable, Authorable, models.Model):
    class EffortRole(models.TextChoices):
        DEVELOPMENT = "D", _("Desarrollo")
        VALIDATION = "V", _("Validación")
        SUPPORT = "S", _("Soporte")

    date = models.DateField(_("fecha"), blank=False, null=False, default=date.today)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario"),
        related_name="effort_allocation",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
    role = models.CharField(_("rol"), choices=EffortRole.choices, blank=False, max_length=1, db_index=True)
    user_story = models.ForeignKey(
        UserStory,
        verbose_name=_("historia de usuario"),
        related_name="effort_allocation",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    effort = models.PositiveSmallIntegerField(
        _("esfuerzo"),
        help_text="Calculado en 'unidades de trabajo'. 1UT = 1/2h.",
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
    )
    comments = models.CharField(_("comentarios"), max_length=2000, blank=True)

    def __str__(self):
        return f"{self.date} / {self.user} / {self.role} / {self.user_story} / {self.effort}"

    class Meta:
        verbose_name = _("asignación de esfuerzo")
        verbose_name_plural = _("asignaciones de esfuerzo")
        ordering = ("-creation_datetime",)
        constraints = [models.UniqueConstraint(fields=["date", "user", "role", "user_story"], name="unique_effort")]


class Task(Uuidable, Orderable, Authorable, models.Model):
    name = models.CharField(_("nombre"), max_length=2000, blank=False)
    user_story = models.ForeignKey(
        UserStory,
        verbose_name=_("historia de usuario"),
        related_name="tasks",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    weight = models.PositiveSmallIntegerField(
        _("peso"), blank=False, null=False, default=1, validators=[MinValueValidator(1)]
    )
    done = models.BooleanField(_("finalizada"), default=False)
    done_changed = MonitorField(_("último cambio en finalizada"), monitor="done")

    order_with_respect_to = ("user_story",)

    def __str__(self):
        return f"{self.user_story} / {self.order}.{self.name} / {self.done}"

    class Meta(Orderable.Meta):
        verbose_name = _("tarea")
        verbose_name_plural = _("tareas")
        constraints = [models.UniqueConstraint(fields=["name", "user_story"], name="unique_task")]
