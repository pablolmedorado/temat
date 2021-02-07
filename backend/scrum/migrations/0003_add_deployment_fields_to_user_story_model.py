from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrum", "0002_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="userstory",
            name="deployment_notes",
            field=models.CharField(blank=True, max_length=2000, verbose_name="notas de despliegue"),
        ),
        migrations.AddField(
            model_name="userstory",
            name="use_migrations",
            field=models.BooleanField(default=False, verbose_name="usa migraciones"),
        ),
    ]
