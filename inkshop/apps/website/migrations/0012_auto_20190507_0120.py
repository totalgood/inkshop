# Generated by Django 2.2.1 on 2019-05-07 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_template_html_extra_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='content_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='hashed_filename',
            field=models.CharField(blank=True, db_index=True, max_length=320, null=True),
        ),
    ]