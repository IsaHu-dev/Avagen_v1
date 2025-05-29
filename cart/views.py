from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """Display the cart page with current session items."""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """Add an item to the cart stored in session."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    cart[item_id] = cart.get(item_id, 0) + quantity
    messages.success(request, f"Added {quantity} of {product.name} to your cart.")

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Update the quantity of an item (or item size) in the session cart."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size', None)
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f"Updated {product.name} ({size.upper()}) to {quantity}.")
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f"Removed size {size.upper()} {product.name} from your cart.")
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f"Updated {product.name} quantity to {quantity}.")
        else:
            cart.pop(item_id)
            messages.success(request, f"Removed {product.name} from your cart.")

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove a product (or a specific size) from the cart, then redirect to product detail page."""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size', None)
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f"Removed {product.name} in size {size.upper()} from your cart.")
        else:
            cart.pop(item_id, None)
            messages.success(request, f"{product.name} has been removed from your cart.")

        request.session['cart'] = cart
        return redirect(f'/products/{item_id}/')  # Redirect to product detail page
    except Exception as error:
        messages.error(request, f"Could not remove item: {error}")
        return redirect(f'/products/{item_id}/')  # Redirect even on failure for user experience