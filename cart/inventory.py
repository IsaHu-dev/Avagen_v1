from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def calculate_delivery_cost(subtotal):
    """
    Calculate delivery cost based on subtotal and free delivery threshold.
    Returns delivery cost and amount needed for free delivery.
    """
    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = subtotal * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - subtotal
    else:
        delivery_cost = 0
        free_delivery_delta = 0
    
    return delivery_cost, free_delivery_delta

def get_cart_items(cart):
    """
    Process cart items and return list of items with their details.
    """
    cart_items = []
    subtotal = 0
    item_count = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        item_total = quantity * product.price
        
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'item_total': item_total,
        })
        
        subtotal += item_total
        item_count += quantity

    return cart_items, subtotal, item_count

def cart_contents(request):
    """
    Make cart contents available across the site.
    Returns a dictionary containing cart information for template context.
    """
    cart = request.session.get('cart', {})
    
    if not cart:
        return {
            'cart_items': [],
            'subtotal': 0,
            'item_count': 0,
            'delivery': 0,
            'free_delivery_delta': settings.FREE_DELIVERY_THRESHOLD,
            'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
            'grand_total': 0,
        }

    cart_items, subtotal, item_count = get_cart_items(cart)
    delivery_cost, free_delivery_delta = calculate_delivery_cost(subtotal)
    grand_total = delivery_cost + subtotal

    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'item_count': item_count,
        'delivery': delivery_cost,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }