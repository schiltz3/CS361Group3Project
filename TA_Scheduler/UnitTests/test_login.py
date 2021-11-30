from django.test import TestCase, Client
from django.shortcuts import reverse
from TA_Scheduler.models import Account


class TestLogin(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.session = self.client.session