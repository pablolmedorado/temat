import taggit.managers

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("common", "0001_initial"),
        ("scrum", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="epic",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.UUIDTaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="sprint",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.UUIDTaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="userstory",
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
