from django.db import migrations


def populate_system_event_types(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    EventType = apps.get_model("events", "EventType")

    holiday, holiday_created = EventType.objects.get_or_create(name="Vacaciones", icon="mdi-beach", system=True)
    support, support_created = EventType.objects.get_or_create(name="Soporte", icon="mdi-face-agent", system=True)
    green, green_created = EventType.objects.get_or_create(
        name="Jornada especial", icon="mdi-briefcase", important=True, system=True
    )
    sprint, sprint_created = EventType.objects.get_or_create(
        name="Sprint", icon="mdi-run-fast", important=True, system=True
    )


class Migration(migrations.Migration):

    dependencies = [("events", "0001_initial")]

    operations = [
        # We set `reverse_code` to `noop` because we cannot revert the
        # migration to get it back in the previous state.
        # If `reverse_code` is not given, the migration will not be
        # reversible, which is not the behaviour we expect here.
        migrations.RunPython(populate_system_event_types, reverse_code=migrations.RunPython.noop)
    ]
