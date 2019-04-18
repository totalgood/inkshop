import logging
import json

from django.urls import reverse
from django.core import mail
from django.conf import settings
from django.test.utils import override_settings

from people.models import Person
from inkmail.models import Subscription
from utils.factory import Factory
from utils.test_helpers import MockRequestsTestCase
from utils.encryption import normalize_lower_and_encrypt, normalize_and_encrypt, encrypt, decrypt
import mock


class TestDoubleOptIn(MockRequestsTestCase):

    def setUp(self, *args, **kwargs):
        self.newsletter = Factory.newsletter()
        super(TestPostSubscribes, self).setUp(*args, **kwargs)

    def test_valid_opt_in_click(self):
        email = Factory.rand_email()
        name = Factory.rand_name()
        self.assertEquals(False, "Test written")

    def test_invalid_opt_in_click(self):
        email = Factory.rand_email()
        name = Factory.rand_name()
        self.assertEquals(False, "Test written")

    def test_clicked_confirm_a_second_time(self):
        email = Factory.rand_email()
        name = Factory.rand_name()
        self.assertEquals(False, "Test written")

    def test_clicked_confirm_over_a_week_later(self):
        email = Factory.rand_email()
        name = Factory.rand_name()
        self.assertEquals(False, "Test written")
