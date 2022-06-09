from django.db import migrations, models

import work_organization.models


def populate_holiday_type_slugs(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    HolidayType = apps.get_model("work_organization", "HolidayType")

    HolidayType.objects.filter(name="General").update(system_slug="GENERAL")
    HolidayType.objects.filter(name="Jornada especial").update(system_slug="GREEN")


def revert_holiday_type_slugs(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    HolidayType = apps.get_model("work_organization", "HolidayType")

    HolidayType.objects.exclude(system_slug__isnull=True).update(system=True)


class Migration(migrations.Migration):

    dependencies = [
        ("work_organization", "0002_populate_system_holiday_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="holidaytype",
            name="system_slug",
            field=models.CharField(
                blank=True,
                choices=[("GENERAL", "General"), ("GREEN", "Jornada especial")],
                db_index=True,
                default=None,
                editable=False,
                max_length=20,
                null=True,
                verbose_name="slug de sistema",
            ),
        ),
        migrations.AlterField(
            model_name="holiday",
            name="type",
            field=models.ForeignKey(
                default=work_organization.models.holiday_type_default,
                on_delete=models.deletion.PROTECT,
                related_name="holidays",
                to="work_organization.holidaytype",
                verbose_name="tipo",
            ),
        ),
        migrations.AddConstraint(
            model_name="holidaytype",
            constraint=models.UniqueConstraint(
                condition=models.Q(("system_slug__isnull", False)),
                fields=("system_slug",),
                name="unique_holiday_type_slug",
            ),
        ),
        migrations.RunPython(populate_holiday_type_slugs, reverse_code=revert_holiday_type_slugs),
        migrations.RemoveField(
            model_name="holidaytype",
            name="system",
        ),
    ]
