# Generated by Django 4.2.11 on 2024-04-04 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_app', '0002_alter_skill_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]