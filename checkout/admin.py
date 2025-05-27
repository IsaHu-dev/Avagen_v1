from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Inline admin for OrderLineItem model"""
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total', 'original_cart',
        'stripe_pid'
    )

    fields = (
        'order_number', 'user', 'date', 'full_name',
        'email', 'phone_number', 'country', 'postcode',
        'town_or_city', 'street_address1', 'street_address2',
        'county', 'delivery_cost', 'order_total', 'grand_total',
        'original_cart', 'stripe_pid'
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost', 'grand_total',
        'status_badge', 'total_items'
    )

    list_filter = ('date', 'country',)
    search_fields = ('order_number', 'full_name', 'email',)
    date_hierarchy = 'date'
    ordering = ('-date',)

    def status_badge(self, obj):
        """Display order status with a colored badge"""
        if obj.stripe_pid:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Paid</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Unpaid</span>'
        )
    status_badge.short_description = 'Payment Status'

    def get_queryset(self, request):
        """Add total items count to queryset"""
        qs = super().get_queryset(request)
        return qs.annotate(
            total_items=Sum('lineitems__quantity')
        )

    def total_items(self, obj):
        """Display total items in order"""
        return obj.total_items
    total_items.short_description = 'Total Items'

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of orders"""
        return False

    def has_add_permission(self, request):
        """Prevent manual order creation"""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow viewing but not editing orders"""
        return request.user.has_perm('checkout.view_order')

    class Media:
        css = {
            'all': ('admin/css/order_admin.css',)
        }


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderLineItem model"""
    list_display = (
        'order_link', 'product_link', 'quantity',
        'lineitem_total'
    )
    list_filter = ('order__date',)
    search_fields = (
        'order__order_number', 'product__name',
        'product__license_number'
    )
    readonly_fields = ('lineitem_total',)

    def order_link(self, obj):
        """Create a link to the order"""
        url = reverse('admin:checkout_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_link.short_description = 'Order'

    def product_link(self, obj):
        """Create a link to the product"""
        url = reverse('admin:products_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Product'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False