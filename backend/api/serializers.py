from rest_framework import serializers

from .models import Product, Order, Customer, OrderItem


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    data = serializers.ModelSerializer(read_only=True)

    class Meta:
        fields = ("message", "data")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderWithItemsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "customer_id", "status", "order_date", "items")
