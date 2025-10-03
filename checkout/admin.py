from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.utils.html import format_html
from .models import Order, OrderLineItem

# Unregister social account models from admin
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.account.models import EmailAddress

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)


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
        'payment_status_colored',
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
            request, f'{updated} order(s) marked as paid.', messages.SUCCESS
        )
    mark_as_paid.short_description = "Mark as PAID"

    def mark_as_failed(self, request, queryset):
        """Mark selected orders as failed"""
        updated = queryset.update(payment_status='failed')
        self.message_user(
            request, f'{updated} order(s) marked as failed.', messages.WARNING
        )
    mark_as_failed.short_description = "Mark as FAILED"

    def payment_status_colored(self, obj):
        """Display payment status with CSS classes"""
        status_classes = {
            'paid': 'payment-status-paid',
            'failed': 'payment-status-failed',
            'pending': 'payment-status-pending'
        }
        css_class = status_classes.get(
            obj.payment_status, 'payment-status-other'
        )
        status_text = obj.get_payment_status_display().upper()
        return format_html(
            '<span class="{}">{}</span>', css_class, status_text
        )
    payment_status_colored.short_description = "Payment Status"
    payment_status_colored.admin_order_field = 'payment_status'

    class Media:
        css = {
            'all': ('css/admin-orders.css',)
        }

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
            request, f'{deleted_count} order(s) deleted successfully.',
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


# Customize admin site headers
admin.site.site_header = "Avagen Admin"
admin.site.site_title = "Avagen Admin Portal"
admin.site.index_title = "Welcome to Avagen Administration"
