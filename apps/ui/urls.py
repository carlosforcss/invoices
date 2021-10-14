# -*- coding: utf-8 -*-
# Django
from django.urls import path
# Third Parties and Python
# - - -
# Project
from apps.ui.views import home


urlpatterns = [
    path("", home, name="home"),
]
