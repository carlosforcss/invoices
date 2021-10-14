# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import serializers
# Product
from apps.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ("id", "created_on", "lines", )
