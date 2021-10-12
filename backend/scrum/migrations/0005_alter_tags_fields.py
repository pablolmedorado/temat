from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_custom_tags"),
        ("scrum", "0004_add_external_resource_field_to_user_story_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="epic",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.TaggedItem",
                to="common.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="sprint",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="common.TaggedItem",
                to="common.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="userstory",
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
