# -*- coding: utf-8 -*-
# Django
from django.db import models
from django.utils.translation import gettext as _
# Python and third parties
from decimal import Decimal
# Product
from apps.utils.models import CommonModel


class Sale(CommonModel):

    discount = models.BooleanField(_("discount"), help_text=_("It applies a 30% discount."), default=False)

    def __str__(self):
        return f"Venta del {self.created_on} por {self.total}"

    @property
    def total(self):
        value = 0
        for sale_line in self.lines.all():
            value += sale_line.value
        if self.discount:
            value = value - (value * Decimal("0.30")).quantize(Decimal("0.00"))
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
    value = models.DecimalField(
        _("value"), max_digits=11,
        decimal_places=2, help_text=_("Product value when sale it's created.")
    )
    amount = models.DecimalField(_("value"), max_digits=11, decimal_places=2, help_text=_("Total amount."))

    def __str__(self):
        return f"{self.name}"

    def __unicode__(self):
        return u"{}".format(self.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.value = self.product.value
            self.amount = self.value * self.quantity
        return super().save(*args, **kwargs)
