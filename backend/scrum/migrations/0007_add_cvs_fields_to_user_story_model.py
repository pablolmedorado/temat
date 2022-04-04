from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrum", "0006_switch_to_currentuserfield"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userstory",
            old_name="cvs_reference",
            new_name="cvs_branch_name",
        ),
        migrations.AlterField(
            model_name="userstory",
            name="cvs_branch_name",
            field=models.CharField(blank=True, max_length=255, verbose_name="rama scv"),
        ),
        migrations.AddField(
            model_name="userstory",
            name="cvs_issue_id",
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name="número de issue"),
        ),
        migrations.AddField(
            model_name="userstory",
            name="cvs_pull_request_id",
            field=models.PositiveIntegerField(
                blank=True, db_index=True, null=True, verbose_name="número de pull request"
            ),
        ),
    ]
