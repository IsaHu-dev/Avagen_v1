"""
Digital Purchase Admin Configuration for Avagen Marketplace
=========================================================

This module configures the Django admin interface for digital purchases
including purchase management, item tracking, and download monitoring.

Author: Isa Hu
Date: 2024
License: MIT License
Original Work: This is original code written specifically for the
Avagen project. No external code was copied or plagiarized.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import DigitalPurchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    """
    Inline admin for purchase items
    """
    model = PurchaseItem
    readonly_fields = [
        'total_price', 'download_count', 'first_downloaded_at', 
        'last_downloaded_at'
    ]
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DigitalPurchase)
class DigitalPurchaseAdmin(admin.ModelAdmin):
    """
    Admin configuration for digital purchases
    """
    list_display = [
        'display_id', 'customer_name', 'customer_email', 
        'payment_status', 'total_amount', 'created_at', 
        'download_status'
    ]
    
    list_filter = [
        'payment_status', 'created_at', 'billing_country',
        ('customer', admin.RelatedOnlyFieldListFilter)
    ]
    
    search_fields = [
        'purchase_id', 'customer_name', 'customer_email',
        'stripe_transaction_id'
    ]
    
    readonly_fields = [
        'purchase_id', 'created_at', 'updated_at', 'subtotal_amount',
        'tax_amount', 'total_amount', 'download_links_display'
    ]
    
    fieldsets = (
        ('Purchase Information', {
            'fields': (
                'purchase_id', 'payment_status', 'stripe_transaction_id',
                'created_at', 'updated_at'
            )
        }),
        ('Customer Details', {
            'fields': (
                'customer', 'customer_name', 'customer_email', 'contact_phone'
            )
        }),
        ('Billing Address', {
            'fields': (
                'billing_country', 'billing_city', 'billing_postal_code',
                'billing_address_line1', 'billing_address_line2', 'billing_state'
            )
        }),
        ('Financial Details', {
            'fields': (
                'subtotal_amount', 'tax_amount', 'total_amount'
            )
        }),
        ('Digital Delivery', {
            'fields': ('download_links_display',)
        }),
        ('Metadata', {
            'fields': ('cart_data',),
            'classes': ('collapse',)
        })
    )
    
    inlines = [PurchaseItemInline]
    
    actions = [
        'mark_as_completed', 'mark_as_failed', 'resend_confirmation_email'
    ]
    
    def display_id(self, obj):
        """Display shortened purchase ID"""
        return obj.display_id
    display_id.short_description = 'Purchase ID'
    display_id.admin_order_field = 'purchase_id'
    
    def download_status(self, obj):
        """Show download status for all items"""
        items = obj.purchase_items.all()
        if not items:
            return 'No items'
        
        total_downloads = sum(item.download_count for item in items)
        total_items = len(items)
        
        if total_downloads == 0:
            return format_html(
                '<span style="color: orange;">Not downloaded</span>'
            )
        elif total_downloads < total_items:
            return format_html(
                '<span style="color: blue;">Partially downloaded</span>'
            )
        else:
            return format_html(
                '<span style="color: green;">Fully downloaded</span>'
            )
    download_status.short_description = 'Download Status'
    
    def download_links_display(self, obj):
        """Display download links for admin"""
        if obj.payment_status != 'completed':
            return 'Payment not completed'
        
        links = obj.get_download_links()
        if not links:
            return 'No download links available'
        
        html_links = []
        for link in links:
            html_links.append(
                f'<li><strong>{link["product_name"]}</strong> - '
                f'<a href="{link["download_url"]}" target="_blank">'
                f'Download ({link["download_count"]} times)</a></li>'
            )
        
        return mark_safe(f'<ul>{"".join(html_links)}</ul>')
    download_links_display.short_description = 'Download Links'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected purchases as completed"""
        updated = queryset.update(payment_status='completed')
        self.message_user(
            request, 
            f'{updated} purchase(s) marked as completed.'
        )
    mark_as_completed.short_description = 'Mark as completed'
    
    def mark_as_failed(self, request, queryset):
        """Mark selected purchases as failed"""
        updated = queryset.update(payment_status='failed')
        self.message_user(
            request, 
            f'{updated} purchase(s) marked as failed.'
        )
    mark_as_failed.short_description = 'Mark as failed'
    
    def resend_confirmation_email(self, request, queryset):
        """Resend confirmation email for selected purchases"""
        from .views import send_purchase_confirmation_email
        
        sent_count = 0
        for purchase in queryset:
            if purchase.payment_status == 'completed':
                try:
                    send_purchase_confirmation_email(purchase)
                    sent_count += 1
                except Exception as e:
                    self.message_user(
                        request, 
                        f'Error sending email for {purchase.display_id}: {e}',
                        level='ERROR'
                    )
        
        self.message_user(
            request, 
            f'Confirmation emails sent for {sent_count} purchase(s).'
        )
    resend_confirmation_email.short_description = 'Resend confirmation emails'
    
    def has_add_permission(self, request):
        """Prevent manual creation of purchases"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of purchases"""
        return False


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for individual purchase items
    """
    list_display = [
        'id', 'purchase_display', 'product_name', 'license_type',
        'quantity', 'unit_price', 'total_price', 'download_count',
        'last_downloaded_at'
    ]
    
    list_filter = [
        'license_type', 'purchase__payment_status', 'purchase__created_at'
    ]
    
    search_fields = [
        'purchase__purchase_id', 'product__name', 'purchase__customer_name'
    ]
    
    readonly_fields = [
        'total_price', 'download_count', 'first_downloaded_at',
        'last_downloaded_at', 'download_link_display'
    ]
    
    fieldsets = (
        ('Item Information', {
            'fields': ('purchase', 'product', 'quantity', 'license_type')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'total_price')
        }),
        ('Download Tracking', {
            'fields': (
                'download_count', 'first_downloaded_at', 'last_downloaded_at',
                'download_link_display'
            )
        })
    )
    
    def purchase_display(self, obj):
        """Display purchase ID with link"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:checkout_digitalpurchase_change', args=[obj.purchase.id]),
            obj.purchase.display_id
        )
    purchase_display.short_description = 'Purchase'
    purchase_display.admin_order_field = 'purchase__purchase_id'
    
    def product_name(self, obj):
        """Display product name with link"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:products_digitalproduct_change', args=[obj.product.id]),
            obj.product.name
        )
    product_name.short_description = 'Product'
    product_name.admin_order_field = 'product__name'
    
    def download_link_display(self, obj):
        """Display download link for admin"""
        if obj.purchase.payment_status != 'completed':
            return 'Payment not completed'
        
        link = obj.get_download_link()
        if not link:
            return 'No download link available'
        
        return format_html(
            '<a href="{}" target="_blank">Download {}</a>',
            link['download_url'], link['product_name']
        )
    download_link_display.short_description = 'Download Link'
    
    def has_add_permission(self, request):
        """Prevent manual creation of purchase items"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of purchase items"""
        return False