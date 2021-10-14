# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
# Project
from apps.inventory.models import Product
from apps.inventory.serializers import ProductSerializer


class ProductPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
