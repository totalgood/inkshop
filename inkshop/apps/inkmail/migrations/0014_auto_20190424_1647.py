# Generated by Django 2.2 on 2019-04-24 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkmail', '0013_outgoingmessage_love_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='internal_name',
            field=models.CharField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]