from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import DigitalProduct


def view_cart(request):
    """Display the cart page with current session items."""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """Add an item to the cart stored in session."""
    product = get_object_or_404(DigitalProduct, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    license_type = request.POST.get('license', 'personal')
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in cart:
        if isinstance(cart[item_id], dict):
            cart[item_id]['quantity'] = (
                cart[item_id].get('quantity', 0) + quantity
            )
        else:
            cart[item_id] = {
                'quantity': quantity,
                'license_type': license_type
            }
    else:
        cart[item_id] = {
            'quantity': quantity,
            'license_type': license_type
        }

    messages.success(
        request,
        f"Added {quantity} of {product.name} to your cart."
    )
    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Update the quantity of an item in the session cart."""
    product = get_object_or_404(DigitalProduct, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    license_type = request.POST.get('license', 'personal')
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = {
            'quantity': quantity,
            'license_type': license_type
        }
        messages.success(
            request,
            f"Updated {product.name} quantity to {quantity}."
        )
    else:
        cart.pop(item_id)
        messages.success(request, f"Removed {product.name} from your cart.")

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove a product from the cart."""
    try:
        product = get_object_or_404(DigitalProduct, pk=item_id)
        cart = request.session.get('cart', {})
        cart.pop(item_id, None)
        messages.success(
            request,
            f"{product.name} has been removed from your cart."
        )
        request.session['cart'] = cart
        return redirect(f'/products/{item_id}/')
    except Exception as error:
        messages.error(request, f"Could not remove item: {error}")
        return redirect(f'/products/{item_id}/')
