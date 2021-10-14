# -*- coding: utf-8 -*-
# Django
from django.urls import include, path
# Third Parties
from rest_framework import routers
# Project
from apps.inventory.views import ProductViewSet

router = routers.DefaultRouter()
router.register("product", ProductViewSet)

urlpatterns = [
    path("", include(router.urls),)
]
