# Generated by Django 4.2.6 on 2023-10-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('alt_phone', models.CharField(max_length=15)),
                ('sex', models.CharField(max_length=50)),
                ('qualification', models.TextField()),
                ('skills', models.TextField()),
                ('experience', models.IntegerField()),
                ('designation', models.CharField(max_length=50)),
                ('expected_ctc', models.FloatField()),
                ('current_ctc', models.FloatField()),
                ('availability', models.BooleanField(default=True)),
                ('notice_period', models.IntegerField()),
                ('current_company', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('resume', models.FileField(blank=True, max_length=200, upload_to='resume/')),
                ('remarks', models.TextField()),
                ('updated_by', models.CharField(max_length=50)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
