from .inventory import cart_contents


def cart_context(request):
    """
    Make cart contents available across the site.
    """
    try:
        return cart_contents(request)
    except Exception:
        # Return empty cart data if there's an error
        return {
            "cart_items": [],
            "subtotal": 0,
            "item_count": 0,
            "grand_total": 0,
        }
