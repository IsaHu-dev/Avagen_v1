from django.db import models
from decimal import Decimal


# Define a model representing product categories
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    is_creator = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products'
    )
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    model_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_price_for_license(self, license_type):
        license_multipliers = {
            'personal': Decimal('1.00'),
            'indie': Decimal('1.15'),  # 15% higher
            'professional': Decimal('1.35'),  # 35% higher
        }
        multiplier = license_multipliers.get(
            license_type.lower(), 
            Decimal('1.00')
        )
        return round(self.base_price * multiplier, 2)

    @property
    def from_price(self):
        return self.get_price_for_license('personal')

    @property
    def personal_price(self):
        return self.get_price_for_license('personal')

    @property
    def indie_price(self):
        return self.get_price_for_license('indie')

    @property
    def professional_price(self):
        return self.get_price_for_license('professional')



















