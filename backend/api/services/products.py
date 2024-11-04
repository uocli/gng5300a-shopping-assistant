from langchain_core.tools import tool

from ..models import Product


@tool
def get_product(product_id: int):
    products = Product.objects.get(id=product_id)
    if products is None:
        return None
    return products[0]


@tool
def search_products(
    name: str = None, category: str = None, limit: int = 20
) -> list[dict]:
    """Search for products based on name and category."""
    products = Product.objects.all()
    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__icontains=category)
    products = products[:limit]
    return products
