from django.contrib import admin
from django.utils.html import format_html
from .models import DigitalProduct, Category

# Register your models here.


class DigitalProductAdmin(admin.ModelAdmin):
    """Admin configuration for DigitalProduct model"""
    
    # Fields to display in the admin list view
    list_display = (
        'name',
        'category',
        'base_price',
        'image',
        'model_number',
        'status',
        'created_at',
        'image_preview',
    )
    
    # Fields that can be edited directly from the list view
    list_editable = ('status',)
    
    # Filter options in the admin sidebar
    list_filter = (
        'status', 
        'category', 
        'created_at',
    )
    
    # Search functionality
    search_fields = ('name', 'description', 'model_number')
    
    # Date hierarchy for better navigation
    date_hierarchy = 'created_at'
    
    # Fields to display in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'model_number')
        }),
        ('Pricing', {
            'fields': ('base_price',)
        }),
        ('Product Type', {
            'fields': ('status',)
        }),
        ('Media', {
            'fields': ('image', 'image_url'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'modified_at', 'image_preview')
    
    # Actions available in the admin
    actions = ['mark_as_published', 'mark_as_draft']
    
    def image_preview(self, obj):
        """Display a preview of the product image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image_url
            )
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def mark_as_published(self, request, queryset):
        """Action to mark selected products as published"""
        updated = queryset.update(status='published')
        self.message_user(
            request, 
            f'{updated} product(s) were successfully marked as published.'
        )
    mark_as_published.short_description = "Mark selected products as published"
    
    def mark_as_draft(self, request, queryset):
        """Action to mark selected products as draft"""
        updated = queryset.update(status='draft')
        self.message_user(
            request, 
            f'{updated} product(s) were successfully marked as draft.'
        )
    mark_as_draft.short_description = "Mark selected products as draft"
    
    def get_queryset(self, request):
        """Custom queryset to show newest products first"""
        return super().get_queryset(request).order_by('-created_at')


class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    
    # Fields shown in the admin list view
    list_display = (
        'friendly_name',
        'name',
        'is_creator',
        'parent',
        'product_count',
    )
    
    # Allow editing is_creator directly from the list view
    list_editable = ('is_creator',)
    
    # Filter options
    list_filter = ('is_creator', 'parent')
    
    # Search functionality
    search_fields = ('name', 'friendly_name')
    
    # Fields to display in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'friendly_name')
        }),
        ('Category Type', {
            'fields': ('is_creator', 'parent')
        }),
    )
    
    def product_count(self, obj):
        """Display the number of products in this category"""
        return obj.products.count()
    product_count.short_description = 'Products Count'


# Register the models with their respective admin configurations
admin.site.register(DigitalProduct, DigitalProductAdmin)
admin.site.register(Category, CategoryAdmin)
