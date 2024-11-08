from django.db import models


class Customer(models.Model):
    """
    A customer model to store the customer's information.
    """

    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Product(models.Model):
    """
    A product model to store the product's information.
    """

    name = models.CharField(max_length=255, null=False, blank=False)
    sku = models.CharField(max_length=255, unique=True, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    category = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    specification = models.TextField()
    quantity_in_store = models.PositiveIntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Order presents both Order itself and Cart in this app according to its status.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            # Cart
            ("draft", "Draft"),
            # Order
            ("ordered", "Ordered"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
    )

    def __str__(self):
        return f"Order {self.id} for {self.customer}"


class OrderItem(models.Model):
    """
    Junction table between Order and Product.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
