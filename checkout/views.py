from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

import stripe
import json

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.inventory import cart_contents


@require_POST
def update_payment_intent(request):
    try:
        payment_id = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            payment_id,
            metadata={
                'cart': json.dumps(request.session.get('cart', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user.username if request.user.is_authenticated else 'guest'
            }
        )
        return HttpResponse(status=200)
    except Exception as error:
        messages.error(request, (
            "Unfortunately, we couldn't process your payment right now. "
            "Please try again shortly."
        ))
        return HttpResponse(content=error, status=400)


def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        current_cart = request.session.get('cart', {})

        order_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'address_line1': request.POST.get('address_line1'),
            'address_line2': request.POST.get('address_line2'),
            'city': request.POST.get('city'),
            'postcode': request.POST.get('postcode'),
            'country': request.POST.get('country'),
        }

        order_form = OrderForm(order_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.stripe_pid = request.POST.get('client_secret').split('_secret')[0]
            order.original_cart = json.dumps(current_cart)

            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item_id, quantity in current_cart.items():
                product = get_object_or_404(Product, pk=item_id)
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            request.session['order_id'] = order.id
            return redirect('checkout_success', order_number=order.order_number)
        else:
            messages.error(request, 'Please check your information and try again.')

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.info(request, 'Your cart is empty.')
            return redirect('products')

        cart_items = cart_contents(request)
        total_amount = cart_items['grand_total']
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),
            currency=settings.STRIPE_CURRENCY
        )

        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret if request.method != 'POST' else None,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(
        request,
        f'Your order {order_number} was successfully processed!'
    )

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)
