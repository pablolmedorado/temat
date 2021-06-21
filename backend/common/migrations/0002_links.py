from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(db_index=True, editable=False, verbose_name="order")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="nombre")),
            ],
            options={
                "verbose_name": "tipo de enlace",
                "verbose_name_plural": "tipos de enlace",
                "ordering": ("order",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(db_index=True, editable=False, verbose_name="order")),
                ("name", models.CharField(max_length=2000, unique=True, verbose_name="nombre")),
                (
                    "icon",
                    models.CharField(
                        help_text="<a href='https://materialdesignicons.com/' target='_blank'>Material Design Icons</a>",
                        max_length=50,
                        verbose_name="icono en la aplicación",
                    ),
                ),
                ("url", models.URLField(max_length=2000, unique=True, verbose_name="url")),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links",
                        to="common.linktype",
                        verbose_name="tipo",
                    ),
                ),
            ],
            options={
                "verbose_name": "enlace",
                "verbose_name_plural": "enlaces",
                "ordering": ("order",),
                "abstract": False,
            },
        ),
    ]
