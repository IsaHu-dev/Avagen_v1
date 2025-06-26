"""
Digital Purchase Models for Avagen Marketplace
==============================================

This module defines the data models for digital product purchases including:
- Purchase transactions
- License assignments
- Digital delivery tracking

Author: Isa Hu
Date: 2024
License: MIT License
Original Work: This is original code written specifically for the
Avagen project. No external code was copied or plagiarized.

Dependencies:
- Django 4.2+
- Stripe (for payment processing)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import hashlib


class DigitalPurchase(models.Model):
    """
    Represents a digital product purchase transaction
    """
    LICENSE_CHOICES = [
        ('personal', 'Personal Use'),
        ('commercial', 'Commercial Use'),
        ('extended', 'Extended License'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('completed', 'Payment Completed'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Unique identifier using UUID instead of timestamp-based
    purchase_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
    # Customer information
    customer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='digital_purchases'
    )
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    contact_phone = models.CharField(max_length=25, blank=True)
    
    # Billing address
    billing_country = models.CharField(max_length=50)
    billing_city = models.CharField(max_length=50)
    billing_postal_code = models.CharField(max_length=20, blank=True)
    billing_address_line1 = models.CharField(max_length=100)
    billing_address_line2 = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=50, blank=True)
    
    # Purchase details
    subtotal_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    
    # Payment tracking
    payment_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    stripe_transaction_id = models.CharField(
        max_length=255, 
        blank=True
    )
    
    # Metadata
    cart_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Digital Purchase'
        verbose_name_plural = 'Digital Purchases'
    
    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.customer_name}"
    
    @property
    def display_id(self):
        """Return a shortened display ID for user-facing references"""
        return str(self.purchase_id)[:8].upper()
    
    def calculate_totals(self):
        """Calculate purchase totals from line items"""
        line_items = self.purchase_items.all()
        subtotal = sum(item.total_price for item in line_items)
        tax_rate = 0.10  # 10% tax rate - could be made configurable
        tax = subtotal * tax_rate
        
        self.subtotal_amount = subtotal
        self.tax_amount = tax
        self.total_amount = subtotal + tax
        self.save()
    
    def mark_as_paid(self, stripe_id):
        """Mark purchase as completed after successful payment"""
        self.payment_status = 'completed'
        self.stripe_transaction_id = stripe_id
        self.save()
    
    def get_download_links(self):
        """Get all download links for purchased items"""
        return [
            item.get_download_link() 
            for item in self.purchase_items.all()
        ]


class PurchaseItem(models.Model):
    """
    Individual items within a digital purchase
    """
    purchase = models.ForeignKey(
        DigitalPurchase,
        on_delete=models.CASCADE,
        related_name='purchase_items'
    )
    product = models.ForeignKey(
        'products.DigitalProduct',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    license_type = models.CharField(
        max_length=20,
        choices=DigitalPurchase.LICENSE_CHOICES,
        default='personal'
    )
    
    # Download tracking
    download_count = models.PositiveIntegerField(default=0)
    first_downloaded_at = models.DateTimeField(null=True, blank=True)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Purchase Item'
        verbose_name_plural = 'Purchase Items'
    
    def __str__(self):
        return f"{self.product.name} - {self.purchase.display_id}"
    
    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        if self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    def get_download_link(self):
        """Generate secure download link for the product"""
        if self.purchase.payment_status != 'completed':
            return None
        
        # Create a secure download token
        token_data = f"{self.purchase.purchase_id}-{self.product.id}-{self.id}"
        download_token = hashlib.sha256(
            token_data.encode()
        ).hexdigest()[:16]
        
        return {
            'product_name': self.product.name,
            'download_url': f"/download/{download_token}/",
            'license_type': self.license_type,
            'download_count': self.download_count
        }
    
    def record_download(self):
        """Record a download attempt"""
        now = timezone.now()
        self.download_count += 1
        
        if not self.first_downloaded_at:
            self.first_downloaded_at = now
        
        self.last_downloaded_at = now
        self.save()
