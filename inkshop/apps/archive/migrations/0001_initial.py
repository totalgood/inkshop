# Generated by Django 2.2 on 2019-04-15 21:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('inkid', models.CharField(blank=True, db_index=True, editable=False, max_length=512, null=True, unique=True)),
                ('salted_inkid', models.CharField(blank=True, db_index=True, editable=False, max_length=512, null=True, unique=True)),
                ('api_jwt_cached', models.CharField(blank=True, editable=False, max_length=512, null=True, unique=True)),
                ('encrypted_first_name', models.CharField(blank=True, max_length=254, null=True)),
                ('encrypted_last_name', models.CharField(blank=True, max_length=254, null=True)),
                ('encrypted_email', models.CharField(blank=True, max_length=254, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('time_zone', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]