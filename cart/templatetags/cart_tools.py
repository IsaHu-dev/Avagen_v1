from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """Calculate the subtotal of an item"""
    return price * quantity


@register.filter(name='get_unit_price')
def get_unit_price(cart_item):
    """Get the unit price for a cart item based on its license type"""
    product = cart_item['product']
    license_type = cart_item['license_type']
    return product.get_price_for_license(license_type) 