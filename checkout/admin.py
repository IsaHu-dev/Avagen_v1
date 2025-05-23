from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin interface for OrderLineItem model.
    Allows viewing and editing line items directly within the Order admin page.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fields = ('product', 'quantity', 'lineitem_total')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.
    Provides a comprehensive view of orders with filtering, search, and inline line items.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid'
    )

    fields = (
        'order_number',
        'user_profile',
        'date',
        'full_name',
        'email',
        'phone_number',
        'country',
        'postcode',
        'town_or_city',
        'street_address1',
        'street_address2',
        'county',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid'
    )

    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    list_filter = (
        'date',
        'country',
        'delivery_cost',
    )

    search_fields = (
        'order_number',
        'full_name',
        'email',
        'phone_number',
        'postcode',
        'town_or_city',
        'street_address1',
        'street_address2',
    )

    ordering = ('-date',)