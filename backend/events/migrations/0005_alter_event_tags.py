import taggit.managers

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_custom_tags"),
        ("events", "0004_eventtype_system_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.TaggedItem",
                to="common.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
