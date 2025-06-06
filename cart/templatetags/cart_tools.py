from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """Calculate the subtotal of an item, safely handling bad input."""
    try:
        price = Decimal(str(price))
    except (InvalidOperation, TypeError, ValueError):
        price = Decimal('0')
    try:
        quantity = Decimal(str(quantity))
    except (InvalidOperation, TypeError, ValueError):
        quantity = Decimal('1')
    return price * quantity

@register.filter
def dict_get(d, key):
    """Safely access dict value by key."""
    if isinstance(d, dict):
        return d.get(key, 1)
    return 1
