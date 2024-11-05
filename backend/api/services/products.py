from langchain_core.tools import tool

from ..models import Product, Order, Customer
from ..serializers import (
    ProductSerializer,
    ResponseSerializer,
    OrderWithItemsSerializer,
)


@tool
def get_product(product_id: int) -> dict:
    """
    Get product by product ID.
    :param product_id:
    :return: a product object
    """
    products = Product.objects.get(id=product_id)
    if products is None:
        return ProductSerializer().data
    return ProductSerializer(products[0]).data


@tool
def search_products(
    name: str = None, category: str = None, limit: int = 20
) -> list[dict]:
    """
    Search for products based on name and category.
    :param name:
    :param category:
    :param limit:
    :return: a list of product objects
    """
    products = Product.objects.all()
    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__icontains=category)
    products = products[:limit]
    return products


@tool
def get_product_by_name(name: str) -> dict:
    """
    Get product by product name.
    :param name:
    :return: a product object
    """
    products = Product.objects.filter(name__icontains=name)
    if products is None:
        return ProductSerializer().data
    return ProductSerializer(products.first()).data


@tool
def get_product_by_category(category: str) -> list[dict]:
    """
    Get product by product category.
    :param category:
    :return: a list of product objects
    """
    products = Product.objects.filter(category__icontains=category)
    if products is None:
        return ProductSerializer().data
    return ProductSerializer(products, many=True).data


@tool
def add_a_product_to_cart(product_id: int, quantity: int, customer_id: int) -> dict:
    """
    Add a product to the cart.
    :param customer_id:
    :param product_id:
    :param quantity:
    :return: a product object
    """
    product = Product.objects.get(id=product_id)
    customer = Customer.objects.get(id=customer_id)
    if product is None:
        return ResponseSerializer(
            {"message": f"Product with ID {product_id} not found.", "data": None}
        ).data
    if customer is None:
        return ResponseSerializer(
            {"message": f"Customer with ID {customer_id} not found.", "data": None}
        ).data
    # TODO: add quantity to product and update it when purchasing
    # product.quantity -= quantity
    # product.save()
    orders = Order.objects.filter(customer_id=customer_id, status="Draft")
    if orders:
        # if there is a draft order, use it.
        # fetch all order items for the order
        order = orders.first()
        order_items = order.items.all()
        for item in order_items:
            if item.product_id == product_id:
                item.quantity += quantity
                item.save()
                return OrderWithItemsSerializer(order).data
    else:
        order = Order.objects.create(customer=customer, status="Draft")
        order.save()
        order_item = order.items.create(
            order=order, product=product, quantity=quantity, price=product.price
        )
        order_item.save()
        print("item2 ==> ", OrderWithItemsSerializer(order).data)
        return OrderWithItemsSerializer(order).data
