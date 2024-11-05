from django.utils import timezone
from langchain_core.tools import tool

from ..models import Customer, Order


@tool
def place_order(customer_id: int) -> dict:
    """
    Place an order for the customer.
    :param customer_id:
    :return: the order details
    """
    customer = Customer.objects.get(id=customer_id)
    if customer is None:
        return {"message": f"Customer with ID {customer_id} not found."}
    elif customer.account_balance <= 0:
        # check the balance of the customer
        return {"message": "Your balance is not enough to place an order."}
    orders = Order.objects.filter(customer_id=customer_id, status="Draft")
    if orders:
        # if there is a draft order (cart), place the order
        order = orders.first()
        # check the balance of the customer and the total price of the order
        total_price = sum(
            [item.product.price * item.quantity for item in order.items.all()]
        )
        if customer.account_balance < total_price:
            return {"message": "Your balance is not enough to place this order."}
        order.status = "Ordered"
        order.order_date = timezone.now()
        order.save()
        # deduct the balance of the customer
        customer.account_balance -= total_price
        customer.save()
        return {"message": "Order placed successfully."}
    else:
        return {"message": "No items can be found in your cart"}
