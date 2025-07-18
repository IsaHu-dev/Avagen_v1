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
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        # Send the email
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle unexpected or unknown webhook events from Stripe
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle successful payment_intent.succeeded events from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_country = shipping_details.address.country
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
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | SUCCESS: '
                    'Verified order already in database'
                ),
                status=200
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

                for item_id, item_data in json.loads(cart).items():
                    product = DigitalProduct.objects.get(id=item_id)
                    if isinstance(item_data, dict):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data['quantity'],
                            license_type=item_data['license_type'],
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
                    content=(
                        f'Webhook received: {event["type"]} | ERROR: {e}'
                    ),
                    status=500
                )

        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | SUCCESS: '
                'Created order in webhook'
            ),
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle failed payments from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
