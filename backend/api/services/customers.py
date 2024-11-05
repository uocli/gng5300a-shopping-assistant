import decimal
import uuid

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from ..core.state import State
from ..models import Customer, Order
from ..serializers import (
    CustomerSerializer,
    OrderItemSerializer,
)


@tool
def fetch_user_and_cart_info(config: RunnableConfig) -> list[dict]:
    """Fetch all items in the cart for the user along with corresponding product information.

    Returns:
        A list of dictionaries where each dictionary contains user balance, the cart details, including the products.
    """
    configuration = config.get("configurable", {})
    customer_id = configuration.get("customer_id", None)
    if not customer_id:
        return [{"message": "No Customer ID configured."}]
    customer = Customer.objects.filter(id=customer_id)
    if customer is None:
        return [{"message": f"Customer with ID {customer_id} not found."}]
    customer = customer.first()
    orders = Order.objects.filter(customer_id=customer_id, status="Draft").all()
    results = [CustomerSerializer(customer).data]
    for order in orders:
        order_to_items = {
            "order_id": order.id,
            "items": [OrderItemSerializer(order.items.all(), many=True).data],
        }
        results.append(order_to_items)

    return results


def user_info(state: State):
    return {"user_info": fetch_user_and_cart_info.invoke({})}


def get_user_info(customer_id: int, thread_id: str) -> dict:
    """
    Get user info by customer ID.
    :param thread_id:
    :param customer_id:
    :return: a dict contains customer_id and thread_id
    """
    users = Customer.objects.filter(id=customer_id)
    if users is None:
        return {
            "customer_id": None,
            "thread_id": None,
        }
    return {
        "customer_id": customer_id,
        "thread_id": str(uuid.uuid4()) if not thread_id else thread_id,
    }


@tool
def add_account_balance(customer_id: int, amount: decimal.Decimal) -> dict:
    """
    Add account balance for the customer.
    :param customer_id:
    :param amount: the amount to add to the account balance
    :return: a dict contains the new account balance
    """
    customer = Customer.objects.get(id=customer_id)
    if customer is None:
        return {"message": f"Customer with ID {customer_id} not found."}
    customer.account_balance += amount
    customer.save()
    user_with_cart = fetch_user_and_cart_info.invoke({customer_id: customer_id})
    return user_with_cart
