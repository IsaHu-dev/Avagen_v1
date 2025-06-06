from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from products.models import Product

def view_cart(request):
    """Display the cart page with current session items."""
    cart = request.session.get('cart', {})
    total = 0
    cleaned_cart = {}

    for item_id, item in cart.items():
        try:
            item_total = float(item['price']) * item.get('quantity', 1)
            total += item_total
            cleaned_cart[item_id] = item
        except KeyError:
            messages.warning(request, f"Cart item {item_id} is missing price and has been skipped.")

    context = {
        'cart': cleaned_cart,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_id):
    """Add a product with selected license to the cart."""
    product = get_object_or_404(Product, pk=item_id)
    license_type = request.POST.get('license', 'personal').lower()
    price = product.get_price_for_license(license_type)
    redirect_url = request.POST.get('redirect_url', reverse('products'))

    cart = request.session.get('cart', {})

    # Store all details needed for cart display
    cart[str(item_id)] = {
        'name': product.name,
        'license': license_type,
        'price': float(price),
        'quantity': 1,  # Default to 1 for now; can expand later
    }

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} ({license_type.title()} License) to your cart.")
    return redirect(redirect_url)


def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        messages.success(request, "Item removed from cart.")
    request.session['cart'] = cart
    return redirect('view_cart')
