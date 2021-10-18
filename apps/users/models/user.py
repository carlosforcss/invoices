# -*- coding: utf-8 -*-
# Django
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from apps.utils.models import CommonModel


class User(CommonModel, AbstractUser):

    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return u"{} {}".format(self.first_name, self.last_name)

    class Meta:
        db_table = _("users")
        verbose_name = _("user")
        verbose_name_plural = _("users")
