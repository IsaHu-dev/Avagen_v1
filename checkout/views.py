from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse,
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from products.models import DigitalProduct

from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.inventory import cart_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "cart": json.dumps(request.session.get("cart", {})),
                "save_info": request.POST.get("save_info"),
                "username": request.user,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. "
            "Please try again later.",
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        cart = request.session.get("cart", {})

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item_id, item_data in cart.items():
                try:
                    product = DigitalProduct.objects.get(id=item_id)
                    if isinstance(item_data, dict):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data["quantity"],
                            license_type=item_data["license_type"],
                        )
                        order_line_item.save()
                    else:
                        messages.error(
                            request,
                            "There was an error with your cart. "
                            "Please try again.",
                        )
                        order.delete()
                        return redirect(reverse("view_cart"))
                except DigitalProduct.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your cart wasn't found in our "
                        "database. Please call us for assistance!",
                    )
                    order.delete()
                    return redirect(reverse("view_cart"))
            # Update the order total after all line items are created

            order.update_total()

            request.session["save_info"] = "save-info" in request.POST
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. "
                "Please double check your information.",
            )

            current_cart = cart_contents(request)
            total = current_cart["grand_total"]
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            return render(
                request,
                "checkout/checkout.html",
                {
                    "order_form": order_form,
                    "stripe_public_key": stripe_public_key,
                    "client_secret": intent.client_secret,
                    "cart_items": current_cart["cart_items"],
                    "total": current_cart["subtotal"],
                    "grand_total": current_cart["grand_total"],
                    "product_count": current_cart["item_count"],
                },
            )
    else:
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(
                request, "There's nothing in your cart at the moment"
            )
            return redirect(reverse("products"))
        current_cart = cart_contents(request)
        total = current_cart["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing. "
                "Did you forget to set it in your environment?",
            )
        template = "checkout/checkout.html"
        context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
            "cart_items": current_cart["cart_items"],
            "total": current_cart["subtotal"],
            "grand_total": current_cart["grand_total"],
            "product_count": current_cart["item_count"],
        }

        return render(request, template, context)


@login_required
def checkout_success(request, order_number):
    """
    Handle successful checkouts - only for the user who made the order
    """
    order = get_object_or_404(Order, order_number=order_number)

    if order.user != request.user:
        messages.error(
            request, "You don't have permission to view this order."
        )
        return redirect("profile")
    messages.success(
        request,
        (
            f"Order successfully processed! Your order number is "
            f"{order_number}. "
            f"A confirmation email will be sent to {order.email}."
        ),
    )

    if "cart" in request.session:
        del request.session["cart"]
    template = "checkout/checkout_success.html"
    context = {
        "order": order,
    }

    return render(request, template, context)
