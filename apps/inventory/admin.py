# -*- coding: utf-8 -*-
# Django
from django.contrib import admin
# Project
from apps.inventory.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value",)


admin.site.register(Product, ProductAdmin)
