from datetime import timedelta
from django.db import migrations


def populate_system_holiday_types(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    HolidayType = apps.get_model("work_organization", "HolidayType")

    holiday, holiday_created = HolidayType.objects.get_or_create(
        name="General", validity=timedelta(days=395), system=True
    )
    green, green_created = HolidayType.objects.get_or_create(
        name="Jornada especial", validity=timedelta(days=60), system=True
    )


class Migration(migrations.Migration):

    dependencies = [("work_organization", "0001_initial")]

    operations = [
        # We set `reverse_code` to `noop` because we cannot revert the
        # migration to get it back in the previous state.
        # If `reverse_code` is not given, the migration will not be
        # reversible, which is not the behaviour we expect here.
        migrations.RunPython(populate_system_holiday_types, reverse_code=migrations.RunPython.noop)
    ]
