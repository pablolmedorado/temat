from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="UUIDTaggedItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.UUIDField(db_index=True, verbose_name="object ID")),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="common_uuidtaggeditem_tagged_items",
                        to="contenttypes.ContentType",
                        verbose_name="content type",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="common_uuidtaggeditem_items",
                        to="taggit.Tag",
                    ),
                ),
            ],
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags",},
        ),
    ]
