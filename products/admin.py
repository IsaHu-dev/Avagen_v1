from django.contrib import admin
from .models import Product, Category

# Register your models here.


# Admin configuration for the Product model
class ProductAdmin(admin.ModelAdmin):
    # Specifies which fields to display in the admin list view
    list_display = (
        'name',
        'base_price',
        'image',
        'model_number',
        'status',
    )
    # Allow editing status directly from the list view
    list_editable = ('status',)
    # Add filter options in the admin sidebar for status
    list_filter = ('status', 'category')
    # Add search functionality
    search_fields = ('name', 'description', 'model_number')


# Admin configuration for the Category model
class CategoryAdmin(admin.ModelAdmin):
    # Fields shown in the admin list view
    list_display = (
        'friendly_name',
        'name',
    )


# Custom admin for Category model with support for 'is_creator' field
class CategoryCreatorAdmin(admin.ModelAdmin):
    # Show 'is_creator' alongside other fields in the list view
    list_display = ('friendly_name', 'name', 'is_creator')
    # Allow editing 'is_creator' directly from the list view
    list_editable = ('is_creator',)
    # Add filter options in the admin sidebar for 'is_creator'
    list_filter = ('is_creator',)


# Register the models with their respective admin configurations
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
