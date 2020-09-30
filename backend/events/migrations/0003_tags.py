from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("common", "0001_initial"),
        ("events", "0002_populate_system_event_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.UUIDTaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
