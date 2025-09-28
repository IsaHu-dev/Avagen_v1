from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from products.models import DigitalProduct


def view_cart(request):
    """Display the cart page with current session items."""
    try:
        from cart.inventory import cart_contents

        current_cart = cart_contents(request)

        context = {
            'cart_items': current_cart['cart_items'],
            'subtotal': current_cart['subtotal'],
            'grand_total': current_cart['grand_total'],
            'item_count': current_cart['item_count'],
        }

        return render(request, 'cart/cart.html', context)
    except Exception as e:
        messages.error(request, f"Error loading cart: {e}")
        return render(request, 'cart/cart.html', {
            'cart_items': [],
            'subtotal': 0,
            'grand_total': 0,
            'item_count': 0,
        })


def add_to_cart(request, item_id):
    """Add an item to the cart stored in session."""
    try:
        product = DigitalProduct.objects.get(pk=item_id)
    except DigitalProduct.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect(reverse("products"))
    quantity = int(request.POST.get('quantity'))
    license_type = request.POST.get('license', 'personal')
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Create unique key combining product ID and license type
    cart_key = f"{item_id}_{license_type}"

    if cart_key in cart:
        cart[cart_key]['quantity'] = (
            cart[cart_key].get('quantity', 0) + quantity
        )
    else:
        cart[cart_key] = {
            'item_id': item_id,
            'quantity': quantity,
            'license_type': license_type
        }

    messages.success(
        request,
        f"Added {quantity} of {product.name} "
        f"({license_type.title()}) to your cart."
    )
    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Update the quantity of an item in the session cart."""
    try:
        product = DigitalProduct.objects.get(pk=item_id)
    except DigitalProduct.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect(reverse("view_cart"))
    quantity = int(request.POST.get('quantity'))
    license_type = request.POST.get('license', 'personal')
    cart = request.session.get('cart', {})

    # Create unique key combining product ID and license type
    cart_key = f"{item_id}_{license_type}"

    if quantity > 0:
        cart[cart_key] = {
            'item_id': item_id,
            'quantity': quantity,
            'license_type': license_type
        }
        messages.success(
            request,
            f"Updated {product.name} ({license_type.title()}) "
            f"quantity to {quantity}."
        )
    else:
        cart.pop(cart_key, None)
        messages.success(
            request,
            f"Removed {product.name} ({license_type.title()}) from your cart."
        )

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove a product from the cart."""
    try:
        product = DigitalProduct.objects.get(pk=item_id)
        license_type = request.POST.get('license', 'personal')
        cart = request.session.get('cart', {})

        # Create unique key combining product ID and license type
        cart_key = f"{item_id}_{license_type}"
        cart.pop(cart_key, None)

        messages.success(
            request,
            f"{product.name} ({license_type.title()}) "
            f"has been removed from your cart."
        )
        request.session['cart'] = cart
        return redirect(reverse('view_cart'))
    except DigitalProduct.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect(reverse('view_cart'))
    except Exception as error:
        messages.error(request, f"Could not remove item: {error}")
        return redirect(reverse('view_cart'))
