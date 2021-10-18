# -*- coding: utf-8 -*-
# Django
from django.test import TestCase, Client
# Python and third parties
from faker import Faker


class CustomTestCase(TestCase):

    client = Client()
    fake = Faker()
