from django.shortcuts import get_object_or_404
from products.models import DigitalProduct


def get_cart_items(cart):
    """
    Process cart items and return list of items with their details.
    """
    cart_items = []
    subtotal = 0
    item_count = 0

    for item_id, item_data in cart.items():
        product = get_object_or_404(DigitalProduct, pk=item_id)
        if isinstance(item_data, dict):
            quantity = item_data["quantity"]
            license_type = item_data["license_type"]
            item_total = quantity * product.get_price_for_license(license_type)

            cart_items.append(
                {
                    "item_id": item_id,
                    "quantity": quantity,
                    "product": product,
                    "license_type": license_type,
                    "item_total": item_total,
                }
            )

            subtotal += item_total
            item_count += quantity
    return cart_items, subtotal, item_count


def cart_contents(request):
    """
    Make cart contents available across the site.
    Returns a dictionary containing cart information for template context.
    """
    cart = request.session.get("cart", {})

    if not cart:
        return {
            "cart_items": [],
            "subtotal": 0,
            "item_count": 0,
            "grand_total": 0,
        }
    cart_items, subtotal, item_count = get_cart_items(cart)
    grand_total = subtotal

    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "item_count": item_count,
        "grand_total": grand_total,
    }
