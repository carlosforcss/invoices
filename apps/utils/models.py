# -*- coding: utf-8 -*-
# Django
from django.db import models
from django.utils.translation import gettext as _


class CommonModel(models.Model):

    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        abstract = True
