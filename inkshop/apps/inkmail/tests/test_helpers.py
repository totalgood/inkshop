import logging
import json

from django.urls import reverse
from django.core import mail
from django.conf import settings
from django.test.utils import override_settings

from people.models import Person
from utils.factory import Factory
from utils.test_helpers import MockRequestsTestCase
from utils.encryption import normalize_lower_and_encrypt, normalize_and_encrypt, encrypt, decrypt
import mock
import unittest

from inkmail.models import Subscription
from inkmail.tasks import queue_next_messages
from inkmail.helpers import send_message, send_newsletter_message, send_transactional_message


class MailTestCase(MockRequestsTestCase):
    def setUp(self, *args, **kwargs):
        super(MailTestCase, self).setUp(*args, **kwargs)

    def create_subscribed_person(self):
        self.subscription = Factory.subscription()
        self.person = self.subscription.person
        self.newsletter = self.subscription.newsletter

    def create_transactional_person(self):
        self.person = Factory.person()

    def send_test_message(self):
        self.test_message = Factory.message()
        self.subject = self.test_message.subject
        self.body = self.test_message.body_text_unrendered
        send_message(message=self.test_message, subscription=self.subscription)
        queue_next_messages()

    def send_newsletter_message(self):
        self.scheduled_newsletter_message = Factory.scheduled_newsletter_message(
            newsletter=self.newsletter,
            send_at_date=self.now(),
            send_at_hour=self.now().hour,
            send_at_minute=self.now().minute,
            use_local_time=False,
        )
        self.subject = self.scheduled_newsletter_message.message.subject
        self.body = self.scheduled_newsletter_message.message.body_text_unrendered
        send_newsletter_message(scheduled_newsletter_message=self.scheduled_newsletter_message)
        queue_next_messages()

    def send_test_transactional_message(self):
        self.transactional_message = Factory.message(person=self.person, transactional=True)
        self.subject = self.transactional_message.subject
        self.body = self.transactional_message.body_text_unrendered
        send_transactional_message(message=self.transactional_message, person=self.person)
        queue_next_messages()


class TestSendMessageMail(MailTestCase):

    def setUp(self, *args, **kwargs):
        self.create_subscribed_person()
        super(TestSendMessageMail, self).setUp(*args, **kwargs)

    def test_send_messsage_sends_to_valid_subscriber(self):
        self.subscription.double_opt_in()
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.test_message.subject)
        self.assertEquals(mail.outbox[0].body, self.test_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, self.newsletter.full_from_email)

    def test_send_messsage_does_not_send_to_unsubscribed(self):
        self.subscription.double_opt_in()
        self.subscription.unsubscribe()
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_not_double_opted_in(self):
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_still_sends_to_trolls(self):
        self.subscription.double_opt_in()
        self.person.mark_troll()
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.test_message.subject)
        self.assertEquals(mail.outbox[0].body, self.test_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, self.newsletter.full_from_email)

    def test_send_messsage_does_not_send_to_banned_people(self):
        self.subscription.double_opt_in()
        self.person.ban()
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_hard_bounce(self):
        self.subscription.double_opt_in()
        m = Factory.message()
        self.person.hard_bounce(bouncing_message=m)
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_hard_bounce_even_if_message_missing(self):
        self.subscription.double_opt_in()
        self.person.hard_bounce()
        self.send_test_message()
        self.assertEquals(len(mail.outbox), 0)


class TestSendNewsletterMessageMail(MailTestCase):

    def setUp(self, *args, **kwargs):
        self.create_subscribed_person()
        super(TestSendNewsletterMessageMail, self).setUp(*args, **kwargs)

    def test_send_messsage_sends_to_valid_subscriber(self):
        self.subscription.double_opt_in()
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.subject)
        self.assertEquals(mail.outbox[0].body, self.body)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, self.newsletter.full_from_email)

    def test_send_messsage_does_not_send_to_unsubscribed(self):
        self.subscription.double_opt_in()
        self.subscription.unsubscribe()
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_not_double_opted_in(self):
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_still_sends_to_trolls(self):
        self.subscription.double_opt_in()
        self.person.mark_troll()
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.subject)
        self.assertEquals(mail.outbox[0].body, self.body)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, self.newsletter.full_from_email)

    def test_send_messsage_does_not_send_to_banned_people(self):
        self.subscription.double_opt_in()
        self.person.ban()
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_hard_bounce(self):
        self.subscription.double_opt_in()
        m = Factory.message()
        self.person.hard_bounce(bouncing_message=m)
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_messsage_does_not_send_to_hard_bounce_even_if_message_missing(self):
        self.subscription.double_opt_in()
        self.person.hard_bounce()
        self.send_newsletter_message()
        self.assertEquals(len(mail.outbox), 0)


class TestSendTransactionalMessageToSubcriber(MailTestCase):

    def setUp(self, *args, **kwargs):
        self.create_subscribed_person()
        super(TestSendTransactionalMessageToSubcriber, self).setUp(*args, **kwargs)

    def test_send_transactional_message_sends_to_valid_subscriber(self):
        self.subscription.double_opt_in()
        self.send_test_transactional_message()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_sends_to_unsubscribed(self):
        self.subscription.double_opt_in()
        self.subscription.unsubscribe()
        self.send_test_transactional_message()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_sends_to_not_double_opted_in(self):
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_sends_to_trolls(self):
        self.subscription.double_opt_in()
        self.person.mark_troll()
        self.send_test_transactional_message()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_does_not_send_to_banned_people(self):
        self.subscription.double_opt_in()
        self.person.ban()
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_transactional_message_does_not_send_to_hard_bounce(self):
        self.subscription.double_opt_in()
        m = Factory.message()
        self.person.hard_bounce(bouncing_message=m)
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_transactional_message_does_not_send_to_hard_bounce_even_if_message_missing(self):
        self.subscription.double_opt_in()
        self.person.hard_bounce()
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)


class TestSendTransactionalMessageToNonSubscriber(MailTestCase):

    def setUp(self, *args, **kwargs):
        self.create_transactional_person()
        super(TestSendTransactionalMessageToNonSubscriber, self).setUp(*args, **kwargs)

    def test_send_transactional_message_sends_to_person(self):
        self.send_test_transactional_message()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_sends_to_trolls(self):
        self.person.mark_troll()
        self.send_test_transactional_message()

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, self.transactional_message.subject)
        self.assertEquals(mail.outbox[0].body, self.transactional_message.body_text_unrendered)
        self.assertEquals(len(mail.outbox[0].to), 1)
        self.assertEquals(mail.outbox[0].to[0], self.person.email)
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_transactional_message_does_not_send_to_banned_people(self):
        self.person.ban()
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_transactional_message_does_not_send_to_hard_bounce(self):
        m = Factory.message()
        self.person.hard_bounce(bouncing_message=m)
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)

    def test_send_transactional_message_does_not_send_to_hard_bounce_even_if_message_missing(self):
        self.person.hard_bounce()
        self.send_test_transactional_message()
        self.assertEquals(len(mail.outbox), 0)
