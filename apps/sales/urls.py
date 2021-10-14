# -*- coding: utf-8 -*-
# Django
from django.urls import include, path
# Third Parties
from rest_framework import routers
# Project
from apps.sales.views import SaleViewSet

router = routers.DefaultRouter()
router.register("sale", SaleViewSet)

urlpatterns = [
    path("", include(router.urls),)
]
