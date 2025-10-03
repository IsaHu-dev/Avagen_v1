from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Inline admin for OrderLineItem"""
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0
    fields = ('product', 'quantity', 'license_type', 'lineitem_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model"""

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'order_total',
        'grand_total',
        'original_cart',
        'stripe_pid',
        'payment_date'
    )

    list_display = (
        'order_number',
        'full_name',
        'email',
        'payment_status',
        'grand_total',
        'date'
    )

    list_filter = (
        'payment_status',
        'date',
        'country'
    )

    search_fields = (
        'order_number',
        'full_name',
        'email'
    )

    ordering = ('-date',)
    list_per_page = 25

    actions = ['mark_as_paid', 'mark_as_failed', 'delete_selected']

    def mark_as_paid(self, request, queryset):
        """Mark selected orders as paid"""
        updated = queryset.update(
            payment_status='paid',
            payment_date=timezone.now()
        )
        self.message_user(
            request,
            f'{updated} order(s) marked as paid.',
            messages.SUCCESS
        )
    mark_as_paid.short_description = "Mark as PAID"

    def mark_as_failed(self, request, queryset):
        """Mark selected orders as failed"""
        updated = queryset.update(payment_status='failed')
        self.message_user(
            request,
            f'{updated} order(s) marked as failed.',
            messages.WARNING
        )
    mark_as_failed.short_description = "Mark as FAILED"

    def delete_selected(self, request, queryset):
        """Custom delete action with warning for paid orders"""
        paid_orders = queryset.filter(payment_status='paid')
        if paid_orders.exists() and not request.user.is_superuser:
            self.message_user(
                request,
                f"Cannot delete {paid_orders.count()} paid order(s). "
                f"Only superusers can delete paid orders.",
                messages.ERROR
            )
            return

        if paid_orders.exists() and request.user.is_superuser:
            self.message_user(
                request,
                f"WARNING: Deleting {paid_orders.count()} paid order(s). "
                f"This action cannot be undone!",
                messages.WARNING
            )
        
        deleted_count = queryset.count()
        queryset.delete()
        self.message_user(
            request,
            f'{deleted_count} order(s) deleted successfully.',
            messages.SUCCESS
        )
    delete_selected.short_description = "Delete selected orders"

    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete any order, prevent deletion of paid 
        orders for regular users"""
        if request.user.is_superuser:
            return True
        if obj and obj.payment_status == 'paid':
            return False
        return super().has_delete_permission(request, obj)


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderLineItem model"""

    list_display = (
        'order',
        'product',
        'quantity',
        'license_type',
        'lineitem_total'
    )

    list_filter = (
        'license_type',
        'order__payment_status'
    )

    search_fields = (
        'order__order_number',
        'product__name'
    )

    readonly_fields = ('lineitem_total',)


# Customize admin site headers
admin.site.site_header = "Avagen Admin"
admin.site.site_title = "Avagen Admin Portal"
admin.site.index_title = "Welcome to Avagen Administration"