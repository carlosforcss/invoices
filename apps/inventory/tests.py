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
from apps.inventory.models import Product


class ProductTestCase(TestCase):

    fake = Faker()
    client = Client()
    BASE_URL = "/api/inventory/product/"

    def setUp(self):
        Product.objects.create(
            name=self.fake.word,
            value=Decimal(random.uniform(0, 1000000)).quantize(Decimal("0.00")),
        )

    def test_get_products(self):
        response = self.client.get(self.BASE_URL)
        product = Product.objects.first()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(type(response.data), ReturnList)
        self.assertEquals(len(response.data), 1)
        product_data = response.data[0]
        self.assertEquals(product_data.get("id"), product.id)
        self.assertEquals(Decimal(product_data.get("value")), product.value)
        self.assertEquals(product_data.get("name"), product.name)

    def test_get_product_detail(self):
        product = Product.objects.first()
        response = self.client.get(f"{self.BASE_URL}{product.id}/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(type(response.data), ReturnDict)
        self.assertEquals(response.data.get("id"), product.id)
        self.assertEquals(Decimal(response.data.get("value")), product.value)
        self.assertEquals(response.data.get("name"), product.name)

    def test_not_allowed_methods(self):
        product = Product.objects.first()
        test_url = f"{self.BASE_URL}{product.id}/"
        fake_data = dict(
            name=self.fake.word(),
            value=Decimal(random.uniform(0, 1000000)).quantize(Decimal("0.00")),
        )
        put_response = self.client.put(test_url, fake_data)
        self.assertEquals(put_response.status_code, status.HTTP_403_FORBIDDEN)
        post_response = self.client.post(test_url, fake_data)
        self.assertEquals(post_response.status_code, status.HTTP_403_FORBIDDEN)
        delete_response = self.client.delete(test_url)
        self.assertEquals(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        patch_response = self.client.patch(test_url, fake_data)
        self.assertEquals(patch_response.status_code, status.HTTP_403_FORBIDDEN)
