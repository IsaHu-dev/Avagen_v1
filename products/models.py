from django.db import models

# Define a model representing product categories
class Category(models.Model):

    # Define meta options for the model
    class Meta:
        # Override the plural name in Django admin (default would be 'Categorys')
        verbose_name_plural = 'Categories'

    # Name of the category (required)
    name = models.CharField(max_length=254)
    
    # Optional user-friendly display name for the category
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    
    # Category for superuser to add new categories dynamically
    is_creator = models.BooleanField(default=False)
    
    # Category for superuser to add new categories dynamically
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.SET_NULL
    )
    
    def __str__(self):
        return self.name

    # Returns the friendly name if available
    def get_friendly_name(self):
        return self.friendly_name


# Define a model representing products
class Product(models.Model):
    # Link each product to a category (optional, set to null if the category is deleted)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)

    # Name of the product (required)
    name = models.CharField(max_length=254)
    
    # Text description of the product (required)
    description = models.TextField()
    
    # Product price with two decimal places (e.g., 9999.99 max if max_digits=6)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Optional field for storing an external image URL
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    
    # Optional field for uploading an image file
    image = models.ImageField(null=True, blank=True)
    
    # Optional field for storing a license number
    license_number = models.CharField(max_length=50, null=True, blank=True)

    # String representation of the product
    def __str__(self):
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars by {self.name}"

