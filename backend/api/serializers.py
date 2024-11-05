from rest_framework import serializers

from .models import Product, Order, Customer, OrderItem


class BaseDataSerializer(serializers.ModelSerializer):
    pass


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    data = BaseDataSerializer(read_only=True)

    class Meta:
        fields = ("message", "data")


class CustomerSerializer(BaseDataSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(BaseDataSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(BaseDataSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderWithItemsSerializer(BaseDataSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "customer_id", "status", "order_date", "items")
