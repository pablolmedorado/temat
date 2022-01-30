from django.conf import settings
from django.db import migrations, models


def migrate_holidays(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Holiday = apps.get_model("work_organization", "Holiday")
    Holiday.objects.filter(green_working_day__isnull=False).update(
        green_working_day_new_id=models.F("green_working_day_id")
    )


def revert_holidays(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Holiday = apps.get_model("work_organization", "Holiday")
    Holiday.objects.filter(green_working_day_new__isnull=False).update(
        green_working_day_id=models.F("green_working_day_new_id")
    )


def migrate_greenworking_days(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("users", "User")
    for user in User.objects.filter(green_working_days_as_main__isnull=False).iterator():
        user.green_working_days.add(*user.green_working_days_as_main.all())
        user.green_working_days_as_main.clear()


def revert_greenworking_days(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("users", "User")
    for user in User.objects.filter(green_working_days__isnull=False).iterator():
        user.green_working_days_as_main.add(*user.green_working_days.all())
        user.green_working_days.clear()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("work_organization", "0004_switch_to_currentuserfield"),
    ]

    operations = [
        migrations.AddField(
            model_name="greenworkingday",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="green_working_days", to=settings.AUTH_USER_MODEL, verbose_name="usuarios"
            ),
        ),
        migrations.AddField(
            model_name="holiday",
            name="green_working_day_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="holiday_new",
                to="work_organization.greenworkingday",
                verbose_name="jornada especial",
            ),
        ),
        migrations.RunPython(migrate_holidays, reverse_code=revert_holidays),
        migrations.RemoveField(
            model_name="holiday",
            name="green_working_day",
        ),
        migrations.RenameField(
            model_name="holiday",
            old_name="green_working_day_new",
            new_name="green_working_day",
        ),
        migrations.AlterField(
            model_name="holiday",
            name="green_working_day",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="holiday",
                to="work_organization.greenworkingday",
                verbose_name="jornada especial",
            ),
        ),
        migrations.RunPython(migrate_greenworking_days, reverse_code=revert_greenworking_days),
        migrations.RemoveField(
            model_name="greenworkingday",
            name="main_user",
        ),
        migrations.RemoveField(
            model_name="greenworkingday",
            name="support_user",
        ),
    ]
