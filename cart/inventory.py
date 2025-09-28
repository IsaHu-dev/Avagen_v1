from products.models import DigitalProduct


def get_cart_items(cart):
    """
    Process cart items and return list of items with their details.
    """
    cart_items = []
    subtotal = 0
    item_count = 0

    for cart_key, item_data in cart.items():
        if isinstance(item_data, dict) and 'item_id' in item_data:
            try:
                item_id = item_data["item_id"]
                product = DigitalProduct.objects.get(pk=item_id)
                quantity = item_data["quantity"]
                license_type = item_data["license_type"]
                item_total = quantity * product.get_price_for_license(
                    license_type
                )

                cart_items.append(
                    {
                        "item_id": item_id,
                        "cart_key": cart_key,
                        "quantity": quantity,
                        "product": product,
                        "license_type": license_type,
                        "item_total": item_total,
                    }
                )

                subtotal += item_total
                item_count += quantity
            except DigitalProduct.DoesNotExist:
                # Skip items that no longer exist in the database
                continue
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

    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "item_count": item_count,
        "grand_total": subtotal,
    }
