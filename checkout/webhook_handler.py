# Import necessary Django modules and models

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Import app-specific models

from .models import Order, OrderLineItem
from products.models import DigitalProduct
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Class to handle Stripe webhooks"""

    def __init__(self, request):
        """Initialize with the request object"""
        self.request = request

    def _send_confirmation_email(self, order):
        """Send order confirmation email to the customer"""
        cust_email = order.email

        # Render email subject and body from templates using the order context
        subject = render_to_string(
            "checkout/confirmation_emails/confirmation_email_subject.txt",
            {"order": order},
        )
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {
                "order": order,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
            },
        )

        # Send the email
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    def handle_event(self, event):
        """Handle unexpected or unknown webhook events from Stripe"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payment_intent.succeeded events from Stripe"""
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        print(f"DEBUG: Webhook received for payment intent {pid}")
        print(f"DEBUG: Cart: {cart}")

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        print(f"DEBUG: Billing email: {billing_details.email}")
        print(f"DEBUG: Grand total: {grand_total}")
        print(f"DEBUG: Shipping name: {shipping_details.name}")

        # Check existing orders
        existing_orders = Order.objects.filter(
            email__iexact=billing_details.email,
            stripe_pid="",
        )
        print(
            "DEBUG: Found "
            f"{existing_orders.count()} orders with email "
            f"{billing_details.email} and empty stripe_pid"
        )
        for order in existing_orders:
            print(
                f"DEBUG: Order {order.order_number} - "
                f"Total: {order.grand_total}, "
                f"Stripe PID: '{order.stripe_pid}'"
            )

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username != "AnonymousUser":
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_country = (
                        shipping_details.address.country
                    )
                    profile.default_phone_number = shipping_details.phone
                    profile.default_postcode = (
                        shipping_details.address.postal_code
                    )
                    profile.default_town_or_city = (
                        shipping_details.address.city
                    )
                    profile.default_street_address1 = (
                        shipping_details.address.line1
                    )
                    profile.default_street_address2 = (
                        shipping_details.address.line2
                    )
                    profile.default_county = shipping_details.address.state
                    profile.save()
            except UserProfile.DoesNotExist:
                profile = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                # First try to find order by stripe_pid
                order = Order.objects.get(stripe_pid=pid)
                order_exists = True
                break
            except Order.DoesNotExist:
                # If not found by stripe_pid, try by email and grand_total
                try:
                    order = Order.objects.get(
                        email__iexact=billing_details.email,
                        grand_total=grand_total,
                        stripe_pid="",  # Look for empty stripe_pid
                    )
                    order.stripe_pid = pid
                    order.update_payment_status("paid")
                    print(
                        f"DEBUG: Updated existing order {order.order_number} "
                        f"with stripe_pid {pid} - Status set to PAID"
                    )
                    print(
                        f"DEBUG: Order stripe_pid after save: "
                        f"'{order.stripe_pid}'"
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    # Try to find any order with same email & total
                    try:
                        order = Order.objects.filter(
                            email__iexact=billing_details.email,
                            grand_total=grand_total,
                        ).first()
                        if order:
                            order.stripe_pid = pid
                            order.update_payment_status("paid")
                            print(
                                f"DEBUG: Updated any order "
                                f"{order.order_number} with stripe_pid {pid} "
                                "- Status set to PAID"
                            )
                            print(
                                f"DEBUG: Order stripe_pid after save: "
                                f"'{order.stripe_pid}'"
                            )
                            order_exists = True
                            break
                    except Exception as e:
                        print(f"DEBUG: Error updating order: {e}")
                        pass
                attempt += 1
                time.sleep(1)

        if order_exists:
            print(f"DEBUG: Order found and updated: {order.order_number}")
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | SUCCESS: '
                    "Verified order already in database"
                ),
                status=200,
            )
        else:
            order = None
            try:
                user = profile.user if profile else None
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user=user,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )

                order.update_payment_status("paid")
                print(
                    f"DEBUG: New order {order.order_number} "
                    "created with PAID status"
                )

                for item_id, item_data in json.loads(cart).items():
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
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500,
                )

        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | SUCCESS: '
                "Created order in webhook"
            ),
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payments from Stripe"""
        intent = event.data.object
        pid = intent.id

        # Find orders with this payment intent and mark as failed
        Order.objects.filter(stripe_pid=pid).update(payment_status="failed")

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
