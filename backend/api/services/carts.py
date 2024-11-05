from django.db.models import Prefetch
from langchain_core.tools import tool

from ..models import Order, OrderItem, Product, Customer
from ..serializers import OrderWithItemsSerializer


@tool
def get_current_cart(customer_id: int) -> dict:
    """
    Get cart info by customer ID.
    :param customer_id:
    :return: the items in the cart of the customer
    """
    carts = Order.objects.filter(
        customer_id=customer_id, status="Draft"
    ).prefetch_related(
        Prefetch("items", queryset=OrderItem.objects.select_related("product"))
    )
    if carts is None:
        return OrderWithItemsSerializer().data
    return OrderWithItemsSerializer(carts.first()).data


@tool
def update_cart(customer_id: int, product_id: int, quantity: int) -> dict:
    """
    Update the quantity of a product in the cart.
    :param customer_id:
    :param product_id:
    :param quantity: the new quantity of the product, 0 means removing the product from the cart
    :return: an updated Cart
    """
    product = Product.objects.get(id=product_id)
    customer = Customer.objects.get(id=customer_id)
    if product is None:
        return {"message": f"Product with ID {product_id} not found."}
    if customer is None:
        return {"message": f"Customer with ID {customer_id} not found."}
    orders = Order.objects.filter(customer_id=customer_id, status="Draft")
    if orders:
        # if there is a draft order (cart), use it, fetch all order items for the order
        cart = orders.first()
        for item in cart.items.all():
            if item.product_id == product_id:
                if quantity == 0:
                    item.delete()
                    if cart.items.count() == 0:
                        cart.delete()
                else:
                    # TODO: if the quantity is more than the available quantity in store, return an error
                    item.quantity = quantity
                    item.save()
    carts = Order.objects.filter(
        customer_id=customer_id, status="Draft"
    ).prefetch_related(
        Prefetch("items", queryset=OrderItem.objects.select_related("product"))
    )
    if carts is None:
        return OrderWithItemsSerializer().data
    return OrderWithItemsSerializer(carts.first()).data


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
    if product is None or product.quantity_in_store < quantity:
        return {"message": f"Product with ID {product_id} not found."}
    if customer is None:
        return {"message": f"Customer with ID {customer_id} not found."}
    orders = Order.objects.filter(customer_id=customer_id, status="Draft")
    if orders:
        # if there is a draft order (cart), use it, fetch all order items for the order
        order = orders.first()
        order_item_exists = False
        for item in order.items.all():
            if item.product_id == product_id:
                order_item_exists = True
                item.quantity += quantity
                item.save()

        if not order_item_exists:
            order_item = order.items.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
                product_name=product.name,
            )
            order_item.save()
    else:
        order = Order.objects.create(customer=customer, status="Draft")
        order.save()
        order_item = order.items.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
            product_name=product.name,
        )
        order_item.save()

    # reduce the quantity of the product in the store
    product.quantity_in_store -= quantity
    product.save()
    carts = Order.objects.filter(
        customer_id=customer_id, status="Draft"
    ).prefetch_related(
        Prefetch("items", queryset=OrderItem.objects.select_related("product"))
    )
    if carts is None:
        return OrderWithItemsSerializer().data
    return OrderWithItemsSerializer(carts.first()).data
