import django_currentuser.db.models.fields
import django_currentuser.middleware

from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0005_alter_event_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="creation_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                blank=True,
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events_event_creations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de creación",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="modification_user",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                on_update=True,
                related_name="events_event_modifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuario de modificación",
            ),
        ),
    ]
