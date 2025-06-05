from django.db import models
from django.core.files.storage import get_storage_class
from django.conf import settings
from products.models import Product

class DigitalDownload(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='digital_downloads/',
        storage=get_storage_class(settings.DIGITAL_DOWNLOAD_STORAGE)(),
        max_length=255
    )
