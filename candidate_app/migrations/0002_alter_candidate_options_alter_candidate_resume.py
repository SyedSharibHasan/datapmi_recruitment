# Generated by Django 4.2.6 on 2023-10-31 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'ordering': ['-updated_on']},
        ),
        migrations.AlterField(
            model_name='candidate',
            name='resume',
            field=models.FileField(blank=True, max_length=200, null=True, upload_to='resume/'),
        ),
    ]
