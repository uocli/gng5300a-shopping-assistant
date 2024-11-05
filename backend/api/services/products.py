from langchain_core.tools import tool

from ..models import Product, Order
from ..helpers.serializers import ProductSerializer


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
        products = products.filter(name__icontains=name, quantity_in_store__gt=0)
    if category:
        products = products.filter(
            category__icontains=category, quantity_in_store__gt=0
        )
    products = products[:limit]
    return ProductSerializer(products, many=True).data


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
def recommend_products(customer_id: int, product_id: int) -> list[dict]:
    """
    Recommend products based on the user's purchase history.
    :param customer_id:
    :param product_id: if provided, recommend products based on this product category, if not, recommend products based on the user's purchase history
    :return: a list of recommended products
    """
    if product_id:
        # if product_id is provided, recommend products based on this product category
        product = Product.objects.get(id=product_id)
        if product is None:
            return [{"message": f"Product with ID {product_id} not found."}]

        products = Product.objects.filter(category__icontains=product.category).all()
        return ProductSerializer(products, many=True).data
    else:
        # if product_id is not provided, recommend products based on the user's purchase history
        purchased_product_id_list = (
            Order.objects.filter(customer_id=customer_id)
            .exclude(status="Draft")
            .values_list("items__product_id", flat=True)
        )

        return ProductSerializer(
            Product.objects.filter(product_in=purchased_product_id_list), many=True
        ).data
