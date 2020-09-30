from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Base",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
            ],
            options={"verbose_name": "base", "verbose_name_plural": "bases", "ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Bread",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
            ],
            options={"verbose_name": "pan", "verbose_name_plural": "panes", "ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Drink",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
            ],
            options={"verbose_name": "bebida", "verbose_name_plural": "bebidas", "ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nombre")),
            ],
            options={"verbose_name": "ingrediente", "verbose_name_plural": "ingredientes", "ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Breakfast",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "base",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="breakfasts",
                        to="breakfasts.Base",
                        verbose_name="base",
                    ),
                ),
                (
                    "bread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="breakfasts",
                        to="breakfasts.Bread",
                        verbose_name="pan",
                    ),
                ),
                (
                    "drink",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="breakfasts",
                        to="breakfasts.Drink",
                        verbose_name="bebida",
                    ),
                ),
                (
                    "ingredient1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="breakfasts_as_first_ingredient",
                        to="breakfasts.Ingredient",
                        verbose_name="primer ingrediente",
                    ),
                ),
                (
                    "ingredient2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="breakfasts_as_second_ingredient",
                        to="breakfasts.Ingredient",
                        verbose_name="segundo ingrediente",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="breakfasts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuario",
                    ),
                ),
            ],
            options={"verbose_name": "desayuno", "verbose_name_plural": "desayunos", "ordering": ("user",)},
        ),
    ]
