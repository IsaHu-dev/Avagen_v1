from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Inline admin for OrderLineItem model"""

    model = OrderLineItem
    readonly_fields = ("lineitem_total",)
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "order_total",
        "grand_total",
        "stripe_pid",
        "payment_date",
    )

    fields = (
        "order_number",
        "user",
        "date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "order_total",
        "grand_total",
        "payment_status",
        "stripe_pid",
        "payment_date",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "payment_status_colored",
        "order_total",
        "grand_total",
    )

    list_filter = (
        "date",
        "payment_status",
    )
    search_fields = (
        "order_number",
        "full_name",
        "email",
    )
    date_hierarchy = "date"
    ordering = ("-date",)


    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete orders"""
        # Superusers can delete orders for administrative purposes
        # This allows cleanup of test orders or unwanted transactions
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Prevent manual order creation"""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow superusers to edit orders"""
        return request.user.is_superuser
    
    def payment_status_colored(self, obj):
        """Display payment status with colour coding"""
        colors = {
            'pending': 'orange',
            'processing': 'blue', 
            'paid': 'green',
            'failed': 'red',
            'cancelled': 'gray'
        }
        
        color = colors.get(obj.payment_status, 'black')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    
    payment_status_colored.short_description = "Payment Status"
    payment_status_colored.admin_order_field = "payment_status"
    
    actions = ['mark_as_paid', 'mark_as_failed', 'delete_orders']
    
    def get_actions(self, request):
        """Remove built-in delete_selected to avoid duplicates"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def mark_as_paid(self, request, queryset):
        """Mark selected orders as paid"""
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = "Mark selected orders as paid"
    
    def mark_as_failed(self, request, queryset):
        """Mark selected orders as failed"""
        updated = queryset.update(payment_status='failed')
        self.message_user(request, f'{updated} orders marked as failed.')
    mark_as_failed.short_description = "Mark selected orders as failed"
    
    def delete_orders(self, request, queryset):
        """Delete selected orders"""
        if not request.user.is_superuser:
            self.message_user(request, 'Only superusers can delete orders.', level='ERROR')
            return
        
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} orders deleted successfully.')
    delete_orders.short_description = "Delete selected orders"

    class Media:
        css = {"all": ("admin/css/order_admin.css",)}


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderLineItem model"""

    list_display = ("order_link", "product_link", "quantity", "lineitem_total")
    list_filter = ("order__date",)
    search_fields = (
        "order__order_number",
        "product__name",
        "product__license_number",
    )
    readonly_fields = ("lineitem_total",)

    def order_link(self, obj):
        """Create a link to the order"""
        url = reverse("admin:checkout_order_change", args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)

    order_link.short_description = "Order"

    def product_link(self, obj):
        """Create a link to the product"""
        url = reverse(
            "admin:products_digitalproduct_change", args=[obj.product.id]
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.name)

    product_link.short_description = "Product"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
