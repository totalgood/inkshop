# Generated by Django 2.2 on 2019-04-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkmail', '0002_auto_20190416_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='double_opted_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='double_opted_in_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]