# Generated by Django 2.2 on 2019-05-06 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20190506_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.Template'),
        ),
    ]