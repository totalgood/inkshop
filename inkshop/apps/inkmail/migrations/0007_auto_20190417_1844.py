# Generated by Django 2.2 on 2019-04-17 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inkmail', '0006_auto_20190417_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='hard_bounced',
        ),
        migrations.RemoveField(
            model_name='newsletter',
            name='hard_bounced_at',
        ),
        migrations.RemoveField(
            model_name='newsletter',
            name='hard_bounced_message',
        ),
    ]
