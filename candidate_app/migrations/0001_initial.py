# Generated by Django 4.2.7 on 2024-01-02 06:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('contact', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=400, upload_to='image/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('client_name', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=150, null=True)),
                ('last_name', models.CharField(max_length=150)),
                ('mode_of_work', models.CharField(default='full_time', max_length=150, null=True)),
                ('gender', models.CharField(blank=True, default='unknown', max_length=50, null=True)),
                ('college', models.CharField(blank=True, max_length=50, null=True)),
                ('graduation_year', models.CharField(blank=True, max_length=50, null=True)),
                ('qualification', models.TextField(blank=True, null=True)),
                ('experience', models.FloatField(blank=True, null=True)),
                ('relevent_experience', models.FloatField(blank=True, null=True)),
                ('designation', models.CharField(blank=True, max_length=50, null=True)),
                ('expected_ctc', models.CharField(blank=True, max_length=50, null=True)),
                ('current_ctc', models.CharField(blank=True, max_length=50, null=True)),
                ('offer_in_hands', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('offer_details', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('notice_period', models.CharField(blank=True, max_length=50, null=True)),
                ('current_company', models.CharField(blank=True, max_length=100, null=True)),
                ('reason_for_change', models.CharField(blank=True, max_length=2000, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('resume', models.FileField(blank=True, max_length=200, null=True, upload_to='resume/')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('screening_time', models.CharField(blank=True, max_length=100, null=True)),
                ('recruiter', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('rejection_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('additional_status', models.CharField(blank=True, max_length=100, null=True)),
                ('rejection_reason_for_r1_r4', models.CharField(blank=True, max_length=100, null=True)),
                ('offer', models.CharField(blank=True, max_length=100, null=True)),
                ('offer_reject_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('skills', models.ManyToManyField(to='candidate_app.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_on'],
            },
        ),
    ]
