import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


def populate_custom_tags(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    TaggitTag = apps.get_model("taggit", "Tag")
    TaggitTaggedItem = apps.get_model("common", "UUIDTaggedItem")

    Tag = apps.get_model("common", "Tag")
    TaggedItem = apps.get_model("common", "TaggedItem")

    tags_dict = {}
    for old_tag in TaggitTag.objects.all().order_by("id").iterator():
        tag, created = Tag.objects.get_or_create(name=old_tag.name, slug=old_tag.slug)
        tags_dict[tag.slug] = tag.pk

    for old_tagged_item in TaggitTaggedItem.objects.select_related("tag").all().iterator():
        TaggedItem.objects.get_or_create(
            object_id=old_tagged_item.object_id,
            content_type_id=old_tagged_item.content_type_id,
            tag_id=tags_dict[old_tagged_item.tag.slug],
        )


def revert_custom_tags(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    TaggitTag = apps.get_model("taggit", "Tag")
    TaggitTaggedItem = apps.get_model("common", "UUIDTaggedItem")

    Tag = apps.get_model("common", "Tag")
    TaggedItem = apps.get_model("common", "TaggedItem")

    tags_dict = {}
    for tag in Tag.objects.all().order_by("id").iterator():
        old_tag, created = TaggitTag.objects.get_or_create(name=tag.name, slug=tag.slug)
        tags_dict[old_tag.slug] = old_tag.pk

    for tagged_item in TaggedItem.objects.select_related("tag").all().iterator():
        TaggitTaggedItem.objects.get_or_create(
            object_id=tagged_item.object_id,
            content_type_id=tagged_item.content_type_id,
            tag_id=tags_dict[tagged_item.tag.slug],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("common", "0002_links"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="slug")),
                (
                    "colour",
                    colorfield.fields.ColorField(
                        blank=True, default="#00AEC7", max_length=18, verbose_name="color en la aplicación"
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        default="mdi-label",
                        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
                        max_length=50,
                        verbose_name="icono en la aplicación",
                    ),
                ),
            ],
            options={
                "verbose_name": "etiqueta",
                "verbose_name_plural": "etiquetas",
            },
        ),
        migrations.CreateModel(
            name="TaggedItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.UUIDField(db_index=True, verbose_name="object ID")),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="common_taggeditem_tagged_items",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="common_taggeditem_items",
                        to="common.tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "ítem etiquetado",
                "verbose_name_plural": "ítems etiquetados",
                "unique_together": {("content_type", "object_id", "tag")},
                "index_together": {("content_type", "object_id")},
            },
        ),
        migrations.RunPython(populate_custom_tags, reverse_code=revert_custom_tags),
    ]
