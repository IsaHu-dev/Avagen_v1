from django.db import models
from django.core.files.storage import get_storage_class
from django.conf import settings
from products.models import DigitalProduct
from django.utils import timezone


class DigitalDownload(models.Model):
    product = models.OneToOneField(
        DigitalProduct, 
        on_delete=models.CASCADE, 
        related_name='digital_download'
    )
    file = models.FileField(
        upload_to='digital_downloads/',
        storage=get_storage_class(settings.DIGITAL_DOWNLOAD_STORAGE)(),
        max_length=500 
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} ({self.product.model_number})"










