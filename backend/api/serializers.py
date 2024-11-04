from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField()

    class Meta:
        model = Order
        fields = ("quantity", "total_price", "order_date", "status")
