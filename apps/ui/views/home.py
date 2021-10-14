# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render
# Third Parties & Python
# - - -
# Project


def home(request):
    template_name = "home.html"
    context = {}
    return render(request, template_name, context)
