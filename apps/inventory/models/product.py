# -*- coding: utf-8 -*-
# Django
from django.db import models
from django.utils.translation import gettext as _
# Product
from apps.utils.models import CommonModel


class Product(CommonModel):

    name = models.CharField(_("name"), max_length=255)
    value = models.DecimalField(_("value"), max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        db_table = _("products")
        verbose_name = _("product")
        verbose_name_plural = _("products")
