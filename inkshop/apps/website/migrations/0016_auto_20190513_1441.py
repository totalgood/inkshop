# Generated by Django 2.2.1 on 2019-05-13 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_link_thumbnail_image_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='url',
            new_name='slug',
        ),
    ]