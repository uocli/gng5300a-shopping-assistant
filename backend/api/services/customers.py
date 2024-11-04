import uuid

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from ..core.state import State
from ..models import Customer, Order
from ..serializers import ProductSerializer


@tool
def fetch_user_order_information(config: RunnableConfig) -> list[dict]:
    """Fetch all orders for the user along with corresponding product information.

    Returns:
        A list of dictionaries where each dictionary contains the ticket details,
        associated flight details, and the seat assignments for each ticket belonging to the user.
    """
    configuration = config.get("configurable", {})
    customer_id = configuration.get("customer_id", None)
    if not customer_id:
        raise ValueError("No Customer ID configured.")

    orders = (
        Order.objects.filter(customer_id=customer_id).prefetch_related("products").all()
    )
    order_items = []
    for order in orders:
        order_to_items = {order.id: [ProductSerializer(order.products, many=True).data]}
        order_items.append(order_to_items)

    # results = OrderSerializer(orders, many=True).data

    return order_items


def user_info(state: State):
    return {"user_info": fetch_user_order_information.invoke({})}


def get_user_info(customer_id: int) -> dict:
    """
    Get user info by customer ID.
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
        "thread_id": str(uuid.uuid4()),
    }
