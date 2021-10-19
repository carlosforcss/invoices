# -*- coding: utf-8 -*-
# Third Parties
from rest_framework import serializers
# Product
from apps.sales.models import Sale, SaleLine
from apps.inventory.models import Product
from apps.utils.serializers import CustomSlugRelatedField


class SaleLineSerializer(serializers.ModelSerializer):

    product = CustomSlugRelatedField(
        queryset=Product.objects.all(),
        slug_field="id",
        additional_fields=[
            "name",
            "value",
        ]
    )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("This field has to be higher tan 0.")
        return value

    class Meta:
        model = SaleLine
        fields = ("id", "product", "quantity", "value", "amount")
        read_only_fields = ("id", "value", "amount", )


class SaleSerializer(serializers.ModelSerializer):

    lines = SaleLineSerializer(many=True)
    total = serializers.DecimalField(read_only=True, max_digits=11, decimal_places=2)

    def validate(self, data):
        lines = data.get("lines")
        if not lines or not len(lines):
            raise serializers.ValidationError("You've got to add at least 1 product.")
        return data

    def create(self, validated_data):
        lines = validated_data.pop("lines")
        new_sale = Sale.objects.create(**validated_data)
        for line_data in lines:
            SaleLine.objects.create(**line_data, sale=new_sale)
        return new_sale

    class Meta:
        model = Sale
        fields = ("id", "created_on", "lines", "discount", "total", )
