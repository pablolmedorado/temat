from django.db import migrations, models


def populate_event_type_slugs(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    EventType = apps.get_model("events", "EventType")

    EventType.objects.filter(name="Vacaciones").update(system_slug="HOLIDAY")
    EventType.objects.filter(name="Soporte").update(system_slug="SUPPORT")
    EventType.objects.filter(name="Jornada especial").update(system_slug="GREEN")
    EventType.objects.filter(name="Sprint").update(system_slug="SPRINT")


def revert_event_type_slugs(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    EventType = apps.get_model("events", "EventType")

    EventType.objects.exclude(system_slug__isnull=True).update(system=True)


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventtype",
            name="system_slug",
            field=models.CharField(
                blank=True,
                choices=[
                    ("HOLIDAY", "Vacaciones"),
                    ("SUPPORT", "Soporte"),
                    ("GREEN", "Jornada especial"),
                    ("SPRINT", "Sprint"),
                ],
                db_index=True,
                default=None,
                editable=False,
                max_length=20,
                null=True,
                verbose_name="slug de sistema",
            ),
        ),
        migrations.AddConstraint(
            model_name="eventtype",
            constraint=models.UniqueConstraint(
                condition=models.Q(("system_slug__isnull", False)), fields=("system_slug",), name="unique_system_slug"
            ),
        ),
        migrations.RunPython(populate_event_type_slugs, reverse_code=revert_event_type_slugs),
        migrations.RemoveField(
            model_name="eventtype",
            name="system",
        ),
    ]
