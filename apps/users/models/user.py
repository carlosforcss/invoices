# -*- coding: utf-8 -*-
# Django
from django.contrib.auth.models import AbstractUser
from apps.utils.models import CommonModel


class User(CommonModel, AbstractUser):

    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return u"{} {}".format(self.first_name, self.last_name)
