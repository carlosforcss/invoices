# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import viewsets
# Product
from apps.sales.models import Sale


class SaleViewSet(viewsets.ModelViewSet):

    queryset = Sale.objects.all()
