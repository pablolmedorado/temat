import django_currentuser.db.models.fields
import django_currentuser.middleware

from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("work_organization", "0003_holidaytype_system_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="greenworkingday",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="work_organization_greenworkingday_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="greenworkingday",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="work_organization_greenworkingday_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="holiday",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="work_organization_holiday_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="holiday",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="work_organization_holiday_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="supportworkingday",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="work_organization_supportworkingday_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="supportworkingday",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="work_organization_supportworkingday_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
    ]
