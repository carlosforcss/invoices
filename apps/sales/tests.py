# -*- coding: utf-8 -*-
# Django
# Python and third parties
import random
from collections import OrderedDict
from decimal import Decimal
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
# Project
from apps.utils.test import CustomTestCase
from apps.sales.models import Sale, SaleLine
from apps.inventory.models import Product


class SaleTestCase(CustomTestCase):

    BASE_URL = "/api/sales/sale/"

    def setUp(self):
        for _ in range(20):
            Product.objects.create(
                name=self.fake.word(),
                value=Decimal(random.uniform(0, 100000)).quantize(Decimal("0.00")),
            )

    def _create_sale(self, discount=False):
        sale = Sale.objects.create(discount=discount)
        products = Product.objects.all()
        for product in products:
            SaleLine.objects.create(
                sale=sale,
                product=product,
                quantity=random.randint(1, 100),
            )
        return sale

    def test_create_sale(self):
        lines = []
        products = Product.objects.all()
        for product in products:
            lines.append(dict(
                product=dict(id=product.id),
                quantity=random.randint(1, 100),
            ))
        sale_data = dict(discount=True, lines=lines)

        # Create sale with and without discount.
        post_response = self.client.post(self.BASE_URL, sale_data, content_type="application/json")
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(type(post_response.data), ReturnDict)
        sale_data["discount"] = False
        post_response_without_discount = self.client.post(self.BASE_URL, sale_data, content_type="application/json")
        self.assertEquals(post_response_without_discount.status_code, status.HTTP_201_CREATED)
        self.assertEquals(type(post_response_without_discount.data), ReturnDict)

        # Check total with discount.
        sale_with_discount = Sale.objects.filter(discount=True).first()
        self.assertEquals(post_response.data.get("id"), sale_with_discount.id)
        sale_with_discount_total = 0
        for line in sale_with_discount.lines.all():
            sale_with_discount_total += line.amount
        sale_with_discount_total -= (sale_with_discount_total * Decimal("0.30")).quantize(Decimal("0.00"))
        self.assertEquals(sale_with_discount_total, sale_with_discount.total)

        # CHeck total without discount.
        sale_without_discount = Sale.objects.filter(discount=False).first()
        self.assertEquals(post_response_without_discount.data.get("id"), sale_without_discount.id)
        sale_without_discount_total = 0
        for line in sale_without_discount.lines.all():
            sale_without_discount_total += line.amount
        self.assertEquals(sale_without_discount_total, sale_without_discount.total)

    def test_get_sales(self):
        new_sale = self._create_sale()
        # Test list endpoint.
        response = self.client.get(f"{self.BASE_URL}")
        self.assertEquals(type(response.data), OrderedDict)
        self.assertEquals(len(response.data.get("results")), 1)
        new_sale_data = response.data.get("results")[0]
        self.assertEquals(new_sale_data.get("id"), new_sale.id)
        self.assertEquals(Decimal(new_sale_data.get("total")), new_sale.total)
        self.assertEquals(len(new_sale_data.get("lines")), new_sale.lines.all().count())

        # Test detail endpoint.
        response_detail = self.client.get(f"{self.BASE_URL}{new_sale.id}/")
        self.assertEquals(type(response_detail.data), ReturnDict)
        self.assertEquals(response_detail.data.get("id"), new_sale.id)
        self.assertEquals(Decimal(response_detail.data.get("total")), new_sale.total)
        self.assertEquals(len(response_detail.data.get("lines")), new_sale.lines.all().count())
