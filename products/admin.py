from django.contrib import admin
from .models import Product, Category, Review


# Admin configuration for the Product model
class ProductAdmin(admin.ModelAdmin):
    """
    Customizes the Product model's admin interface.
    Displays key product information in the list view.
    """
    list_display = (
        'name',        # Product name
        'category',    # Associated category
        'price',       # Product price
        'image',       # Product image
        'license_number', # Product license number
    )
    search_fields = ('name', 'category__name', 'license_number')
    

# Admin configuration for the Category model
class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the Category model's admin interface.
    Shows both friendly and internal names in the list view.
    """
    list_display = (
        'friendly_name',  # User-friendly display name
        'name',          # Internal category name
    )


# Admin configuration for Category with creator / admin functionality
class CategoryCreatorAdmin(admin.ModelAdmin):
    """
    Extended Category admin interface with creator-specific features.
    Allows filtering and editing of creator status.
    """
    list_display = ('friendly_name', 'name', 'is_creator')  # Display fields
    list_editable = ('is_creator',)  # Allow inline editing of creator status
    list_filter = ('is_creator',)    # Add filter for creator status


# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    """
    Customizes the Review model's admin interface.
    Shows review details including product, reviewer, rating, and timestamp.
    """
    list_display = (
        'product',     # Reviewed product
        'name',        # Reviewer's name
        'rating',      # Star rating (1-5)
        'created_at',  # Review timestamp
    )


# Register models with their custom admin configurations
admin.site.register(Product, ProductAdmin)    # Register Product model
admin.site.register(Category, CategoryAdmin)  # Register Category model
admin.site.register(Review, ReviewAdmin)      # Register Review model