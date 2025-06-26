"""
Digital Purchase Views for Avagen Marketplace
============================================

This module handles digital product purchase functionality including:
- Purchase initiation and processing
- Payment handling with Stripe
- Digital delivery management
- Purchase confirmation

Author: Isa Hu
Date: 2024
License: MIT License
Original Work: This is original code written specifically for the
Avagen project. No external code was copied or plagiarized.

Dependencies:
- Django 4.2+
- Stripe (for payment processing)
- django-allauth
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import DigitalProduct

from .forms import UserInfoForm, LicenseSelectionForm, UserCheckoutForm
from .models import DigitalPurchase, PurchaseItem
from cart.inventory import cart_contents

import stripe
import json
import logging

logger = logging.getLogger(__name__)


@require_POST
def prepare_payment_intent(request):
    """
    Prepare Stripe payment intent with purchase metadata
    """
    try:
        # Extract payment intent ID from client secret
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            return JsonResponse(
                {'error': 'Client secret is required'}, 
                status=400
            )
        
        payment_intent_id = client_secret.split('_secret')[0]
        
        # Configure Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Get cart data
        cart_data = request.session.get('cart', {})
        
        # Update payment intent with metadata
        stripe.PaymentIntent.modify(
            payment_intent_id,
            metadata={
                'cart_items': json.dumps(cart_data),
                'save_billing_info': request.POST.get('save_billing_info', 'false'),
                'customer_id': str(request.user.id) if request.user.is_authenticated else '',
                'purchase_type': 'digital_products'
            }
        )
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Error preparing payment intent: {str(e)}")
        messages.error(
            request,
            'Unable to process payment request. Please try again.'
        )
        return JsonResponse(
            {'error': 'Payment processing error'}, 
            status=500
        )


def initiate_purchase(request):
    """
    Handle the purchase initiation process
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    # Check if cart has items
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty')
        return redirect('products')
    
    if request.method == 'POST':
        # Handle form submission
        user_info_form = UserInfoForm(request.POST)
        license_form = LicenseSelectionForm(request.POST)
        
        if user_info_form.is_valid() and license_form.is_valid():
            try:
                # Create purchase record
                purchase = user_info_form.save(commit=False)
                
                # Set customer if authenticated
                if request.user.is_authenticated:
                    purchase.customer = request.user
                
                # Save cart data
                purchase.cart_data = cart
                purchase.save()
                
                # Create purchase items
                for product_id, item_data in cart.items():
                    try:
                        product = DigitalProduct.objects.get(id=product_id)
                        
                        if isinstance(item_data, dict):
                            # Create purchase item
                            purchase_item = PurchaseItem(
                                purchase=purchase,
                                product=product,
                                quantity=item_data.get('quantity', 1),
                                license_type=item_data.get('license_type', 'personal'),
                                unit_price=product.get_price_for_license(
                                    item_data.get('license_type', 'personal')
                                )
                            )
                            purchase_item.save()
                        else:
                            raise ValueError("Invalid cart item format")
                            
                    except DigitalProduct.DoesNotExist:
                        messages.error(
                            request,
                            f'Product with ID {product_id} not found'
                        )
                        purchase.delete()
                        return redirect('view_cart')
                
                # Calculate totals
                purchase.calculate_totals()
                
                # Store purchase ID in session
                request.session['current_purchase_id'] = str(purchase.purchase_id)
                
                # Redirect to payment confirmation
                return redirect('confirm_payment', purchase_id=purchase.purchase_id)
                
            except Exception as e:
                logger.error(f"Error creating purchase: {str(e)}")
                messages.error(
                    request,
                    'Error processing your purchase. Please try again.'
                )
                return redirect('view_cart')
        else:
            # Form validation failed
            messages.error(
                request,
                'Please correct the errors in your form.'
            )
    
    # GET request or form validation failed
    current_cart = cart_contents(request)
    total_amount = current_cart['grand_total']
    
    # Create Stripe payment intent
    try:
        stripe.api_key = stripe_secret_key
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),  # Convert to cents
            currency=settings.STRIPE_CURRENCY,
            metadata={'purchase_type': 'digital_products'}
        )
        
        client_secret = payment_intent.client_secret
        
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}")
        messages.error(
            request,
            'Unable to initialize payment system. Please try again.'
        )
        return redirect('view_cart')
    
    # Initialize forms
    user_form = UserCheckoutForm()
    user_info_form = UserInfoForm()
    license_form = LicenseSelectionForm()
    
    # Pre-populate form if user is authenticated
    if request.user.is_authenticated:
        user_info_form.fields['customer_name'].initial = (
            f"{request.user.first_name} {request.user.last_name}".strip()
        )
        user_info_form.fields['customer_email'].initial = request.user.email
    
    context = {
        'user_form': user_form,
        'user_info_form': user_info_form,
        'license_form': license_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
        'cart_total': total_amount,
        'cart_items': current_cart['cart_items']
    }
    
    return render(request, 'checkout/checkout.html', context)


def confirm_payment(request, purchase_id):
    """
    Display payment confirmation page
    """
    try:
        purchase = get_object_or_404(DigitalPurchase, purchase_id=purchase_id)
        
        # Verify this purchase belongs to the current user
        if request.user.is_authenticated and purchase.customer != request.user:
            messages.error(request, 'Access denied')
            return redirect('products')
        
        context = {
            'purchase': purchase,
            'purchase_items': purchase.purchase_items.all(),
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        }
        
        return render(request, 'checkout/payment_confirmation.html', context)
        
    except Exception as e:
        logger.error(f"Error in payment confirmation: {str(e)}")
        messages.error(request, 'Error loading payment confirmation')
        return redirect('view_cart')


@csrf_exempt
def process_payment_webhook(request):
    """
    Handle Stripe webhook for payment confirmation
    """
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    # Get the webhook secret and payload
    webhook_secret = settings.STRIPE_WH_SECRET
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    
    return HttpResponse(status=200)


def handle_successful_payment(payment_intent):
    """
    Process successful payment
    """
    try:
        # Extract purchase ID from metadata
        purchase_id = payment_intent.metadata.get('purchase_id')
        if not purchase_id:
            logger.error("No purchase ID in payment metadata")
            return
        
        # Get purchase and mark as paid
        purchase = DigitalPurchase.objects.get(purchase_id=purchase_id)
        purchase.mark_as_paid(payment_intent.id)
        
        # Send confirmation email
        send_purchase_confirmation_email(purchase)
        
        logger.info(f"Payment successful for purchase {purchase_id}")
        
    except DigitalPurchase.DoesNotExist:
        logger.error(f"Purchase {purchase_id} not found")
    except Exception as e:
        logger.error(f"Error processing successful payment: {str(e)}")


def handle_failed_payment(payment_intent):
    """
    Process failed payment
    """
    try:
        purchase_id = payment_intent.metadata.get('purchase_id')
        if purchase_id:
            purchase = DigitalPurchase.objects.get(purchase_id=purchase_id)
            purchase.payment_status = 'failed'
            purchase.save()
            
            logger.info(f"Payment failed for purchase {purchase_id}")
            
    except DigitalPurchase.DoesNotExist:
        logger.error(f"Purchase {purchase_id} not found")
    except Exception as e:
        logger.error(f"Error processing failed payment: {str(e)}")


def purchase_success(request, purchase_id):
    """
    Display purchase success page
    """
    try:
        purchase = get_object_or_404(DigitalPurchase, purchase_id=purchase_id)
        
        # Verify ownership
        if request.user.is_authenticated and purchase.customer != request.user:
            messages.error(request, 'Access denied')
            return redirect('products')
        
        # Clear cart
        if 'cart' in request.session:
            del request.session['cart']
        
        # Clear current purchase from session
        if 'current_purchase_id' in request.session:
            del request.session['current_purchase_id']
        
        messages.success(
            request,
            f'Purchase completed successfully! '
            f'Your purchase ID is {purchase.display_id}. '
            f'Download links have been sent to {purchase.customer_email}.'
        )
        
        context = {
            'purchase': purchase,
            'download_links': purchase.get_download_links()
        }
        
        return render(request, 'checkout/purchase_success.html', context)
        
    except Exception as e:
        logger.error(f"Error in purchase success: {str(e)}")
        messages.error(request, 'Error loading purchase details')
        return redirect('products')


def send_purchase_confirmation_email(purchase):
    """
    Send purchase confirmation email with download links
    """
    try:
        subject = f'Purchase Confirmation - {purchase.display_id}'
        
        # Prepare email context
        context = {
            'purchase': purchase,
            'download_links': purchase.get_download_links(),
            'purchase_items': purchase.purchase_items.all()
        }
        
        # Render email templates
        html_message = render_to_string(
            'checkout/emails/purchase_confirmation.html', 
            context
        )
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[purchase.customer_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Confirmation email sent for purchase {purchase.purchase_id}")
        
    except Exception as e:
        logger.error(f"Error sending confirmation email: {str(e)}")


@login_required
def purchase_history(request):
    """
    Display user's purchase history
    """
    purchases = DigitalPurchase.objects.filter(
        customer=request.user
    ).order_by('-created_at')
    
    context = {
        'purchases': purchases
    }
    
    return render(request, 'checkout/purchase_history.html', context)
