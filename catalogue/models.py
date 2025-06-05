from django.db import models
from products.models import Product

class DigitalDownload(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='download')
    file = models.FileField(upload_to='digital_downloads/', max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download for {self.product.name} ({self.product.model_number})"
