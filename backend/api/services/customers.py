import uuid

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from ..core.state import State
from ..models import Customer, Order
from ..serializers import ProductSerializer, CustomerSerializer


@tool
def fetch_user_order_information(config: RunnableConfig) -> list[dict]:
    """Fetch all orders for the user along with corresponding product information.

    Returns:
        A list of dictionaries where each dictionary contains the order details, including the products.
    """
    configuration = config.get("configurable", {})
    customer_id = configuration.get("customer_id", None)
    if not customer_id:
        raise ValueError("No Customer ID configured.")
    customer = Customer.objects.filter(id=customer_id)
    if customer is None:
        raise ValueError(f"Customer with ID {customer_id} not found.")
    customer = customer.first()

    orders = (
        Order.objects.filter(customer_id=customer_id).prefetch_related("products").all()
    )
    results = [CustomerSerializer(customer).data]
    for order in orders:
        order_to_items = {order.id: [ProductSerializer(order.products, many=True).data]}
        results.append(order_to_items)

    return results


def user_info(state: State):
    return {"user_info": fetch_user_order_information.invoke({})}


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
