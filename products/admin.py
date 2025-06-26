from django.contrib import admin
from django.utils.html import format_html
from .models import DigitalProduct, Category
from django import forms


class DigitalProductAdminForm(forms.ModelForm):
    """Custom form for DigitalProduct with proper image field configuration"""
    
    class Meta:
        model = DigitalProduct
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
        }


class DigitalProductAdmin(admin.ModelAdmin):
    """Admin configuration for DigitalProduct with working image upload"""
    
    form = DigitalProductAdminForm
    
    list_display = (
        'name',
        'category',
        'base_price',
        'model_number',
        'status',
        'created_at',
        'image_preview',
    )
    list_editable = ('status',)
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'description', 'model_number')
    date_hierarchy = 'created_at'

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
            'description': 'Upload a product image or provide an image URL.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'modified_at', 'image_preview')

    def image_preview(self, obj):
        """Display thumbnail preview of image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 60px; '
                'object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 60px; '
                'border-radius: 4px;" />',
                obj.image_url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'

    actions = ['mark_as_published', 'mark_as_draft']

    def mark_as_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(
            request, 
            f'{updated} product(s) marked as published.'
        )
    mark_as_published.short_description = "Mark selected as published"

    def mark_as_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(
            request, 
            f'{updated} product(s) marked as draft.'
        )
    mark_as_draft.short_description = "Mark selected as draft"

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'is_creator',
        'parent',
        'product_count',
    )
    list_editable = ('is_creator',)
    list_filter = ('is_creator', 'parent')
    search_fields = ('name', 'friendly_name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'friendly_name')
        }),
        ('Category Type', {
            'fields': ('is_creator', 'parent')
        }),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products Count'


admin.site.register(DigitalProduct, DigitalProductAdmin)
admin.site.register(Category, CategoryAdmin)
