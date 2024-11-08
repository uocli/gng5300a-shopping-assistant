from rest_framework import serializers

from ..models import Product, Order, Customer, OrderItem


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer Serializer
    """

    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer
    """

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order Item Serializer
    """

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderWithItemsSerializer(serializers.ModelSerializer):
    """
    Order Serializer with Order Items
    """

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "customer_id", "status", "order_date", "items")
