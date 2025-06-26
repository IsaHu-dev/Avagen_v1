from django.db import models
from products.models import DigitalProduct


class Review(models.Model):
    product = models.ForeignKey(
        DigitalProduct,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    name = models.CharField(max_length=100)
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # 1–5 stars
    comment = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars by {self.name}"
