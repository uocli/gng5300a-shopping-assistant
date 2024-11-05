from langchain_core.tools import tool

from ..models import Product
from ..serializers import ProductSerializer


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
