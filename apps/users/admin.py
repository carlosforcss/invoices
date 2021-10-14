# -*- coding: utf-8 -*-
# Django
from django.contrib import admin
# Project
from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "created_on")


admin.site.register(User, UserAdmin)
