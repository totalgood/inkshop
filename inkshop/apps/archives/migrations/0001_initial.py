# Generated by Django 2.2 on 2019-04-26 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('event_type', models.CharField(blank=True, max_length=254, null=True)),
                ('event_creator_type', models.CharField(blank=True, max_length=254, null=True)),
                ('event_creator_pk', models.IntegerField(blank=True, null=True)),
                ('encrypted_json_event_data', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
