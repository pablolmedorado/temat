from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_alter_event_tags"),
        ("scrum", "0005_alter_tags_fields"),
        ("common", "0003_custom_tags"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UUIDTaggedItem",
        ),
    ]
