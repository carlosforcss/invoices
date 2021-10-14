# -*- coding: utf-8 -*-
# Django
from django.db import models
from django.utils.translation import gettext as _
# Product
from apps.utils.models import CommonModel


class Sale(CommonModel):

    def __str__(self):
        return f"Venta del {self.created_on} por {self.total}"

    @property
    def total(self):
        value = 0
        for sale_line in self.lines.all():
            value += sale_line.value
        return value


class SaleLine(CommonModel):

    sale = models.ForeignKey(
        "sales.Sale", related_name="lines",
        verbose_name=_("sale"), on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "inventory.Product",
        related_name="sales",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField("quantity")

    def __str__(self):
        return f"{self.name}"

    def __unicode__(self):
        return u"{}".format(self.name)
