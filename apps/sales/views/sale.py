# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
# Product
from apps.sales.models import Sale
from apps.sales.serializers import SaleSerializer


class SalePermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        return False


class SaleViewSet(viewsets.ModelViewSet):

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [SalePermissions]
