from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.

# Admin configuration for the Product model
class ProductAdmin(admin.ModelAdmin):
    # Specifies which fields to display in the admin list view
    list_display = (
        'name',
        'category',
        'price',
        'image',
    )

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

# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    # Display fields for reviews in the admin list view
    list_display = (
        'product',
        'name',
        'rating',
        'created_at',
    )

# Register the models with their respective admin configurations
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
