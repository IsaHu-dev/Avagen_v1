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
        "payment_status",
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
        """Prevent deletion of orders"""
        return False

    def has_add_permission(self, request):
        """Prevent manual order creation"""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow viewing but not editing orders"""
        return request.user.has_perm("checkout.view_order")
    
    actions = ['mark_as_paid', 'mark_as_failed']
    
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
