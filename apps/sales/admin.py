# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.sales.models import Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "total", "created_on", "discount", )


admin.site.register(Sale, SaleAdmin)
