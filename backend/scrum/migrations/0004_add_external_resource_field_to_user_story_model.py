import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrum", "0003_add_deployment_fields_to_user_story_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="userstory",
            name="external_resource",
            field=models.CharField(
                blank=True,
                help_text="Ruta a un fichero o directorio con recursos externos",
                max_length=2000,
                validators=[django.core.validators.URLValidator(schemes=["http", "https", "file", "ftp", "ftps"])],
                verbose_name="recurso externo",
            ),
        ),
    ]
