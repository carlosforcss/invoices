# -*- coding: utf-8 -*-
# Django
from django.test import TestCase, Client
# Python and third parties
from faker import Faker
import random
from decimal import Decimal
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
# Project
from apps.sales.models import Sale
from apps.inventory.models import Product


class SaleTestCase(TestCase):

    fake = Faker()
    client = Client()
    BASE_URL = "/api/sales/sale/"

    def setUp(self):
        for _ in range(20):
            Product.objects.create(
                name=self.fake.word(),
                value=Decimal(random.uniform(0, 100000)).quantize(Decimal("0.00")),
            )

    def test_create_sale(self):
        has_discount = random.random() > 0.5
        lines = []
        product = Product.objects.first()
        lines.append(dict(
            product=product.id,
            quantity=random.randint(1, 100),
        ))
        product = Product.objects.last()
        lines.append(dict(
            product=product.id,
            quantity=random.randint(1, 100),
        ))
        sale_data = dict(discount=has_discount, lines=lines)
        response = self.client.post(self.BASE_URL, sale_data
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_sales(self):
        pass

    def test_delete_sale(self):
        pass
