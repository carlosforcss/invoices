# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import serializers
# Project
from apps.inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "name", "value", )
