# Generated by Django 2.2 on 2019-04-22 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inkmail', '0004_outgoingmessage_unsubscribe_hash'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScheduledMessage',
            new_name='ScheduledNewsletterMessage',
        ),
        migrations.RemoveField(
            model_name='outgoingmessage',
            name='scheduled_message',
        ),
        migrations.RemoveField(
            model_name='outgoingmessageattempttombstone',
            name='outgoing_message',
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='attempt_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='attempt_started',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='hard_bounce_reason',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='hard_bounced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inkmail.Message'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='retry_if_not_complete_by',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='scheduled_newsletter_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inkmail.ScheduledNewsletterMessage'),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='send_success',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='subscription',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inkmail.Subscription'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='transactional',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='outgoingmessageattempttombstone',
            name='outgoing_message_pk',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outgoingmessageattempttombstone',
            name='retry_number',
            field=models.IntegerField(default=0),
        ),
    ]
