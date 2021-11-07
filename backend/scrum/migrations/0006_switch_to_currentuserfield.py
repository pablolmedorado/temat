from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("scrum", "0005_alter_tags_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="effort",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_effort_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="effort",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_effort_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="epic",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_epic_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="epic",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_epic_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="progress",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_progress_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="progress",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_progress_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="sprint",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_sprint_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="sprint",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_sprint_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_task_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_task_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
        migrations.AlterField(
            model_name="userstory",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="scrum_userstory_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="userstory",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="scrum_userstory_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
    ]
