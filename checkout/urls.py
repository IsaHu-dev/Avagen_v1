"""
Digital Purchase URL Configuration for Avagen Marketplace
=======================================================

This module defines URL patterns for digital product purchases including:
- Purchase initiation
- Payment processing
- Purchase confirmation and history

Author: Isa Hu
Date: 2024
License: MIT License
Original Work: This is original code written specifically for the
Avagen project. No external code was copied or plagiarized.
"""

from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    # Purchase initiation
    path('initiate/', views.initiate_purchase, name='initiate_purchase'),
    
    # Payment processing
    path('prepare-payment/', views.prepare_payment_intent, 
         name='prepare_payment_intent'),
    path('confirm/<uuid:purchase_id>/', views.confirm_payment, 
         name='confirm_payment'),
    
    # Webhook handling
    path('webhook/', views.process_payment_webhook, 
         name='process_payment_webhook'),
    
    # Success and history
    path('success/<uuid:purchase_id>/', views.purchase_success, 
         name='purchase_success'),
    path('history/', views.purchase_history, name='purchase_history'),
] 