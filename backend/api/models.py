from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    sku = models.CharField(max_length=255, unique=True, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.CharField(max_length=255, null=False)
    description = models.TextField()
    specification = models.TextField()

    def __str__(self):
        return self.name


# Draft, Ordered, Shipped, Delivered, Cancelled
class OrderStatus(models.TextChoices):
    DRAFT = "D", "draft"
    ORDERED = "O", "ordered"
    SHIPPED = "S", "shipped"
    DELIVERED = "E", "delivered"
    CANCELLED = "C", "cancelled"


class Order(models.Model):
    customer_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=1, choices=OrderStatus.choices, default=OrderStatus.DRAFT
    )

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Cart(models.Model):
    items = models.ManyToManyField(Order)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} items in cart"
