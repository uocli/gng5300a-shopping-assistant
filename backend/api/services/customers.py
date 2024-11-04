import uuid
from ..models import Customer


def get_user_info(customer_id: str) -> dict:
    users = Customer.objects.get(id=customer_id)
    if users is None:
        return {
            "customer_id": None,
            "thread_id": None,
        }
    return {
        "customer_id": "1234",
        "thread_id": str(uuid.uuid4()),
    }
