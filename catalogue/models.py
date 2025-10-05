from django.db import models
from django.core.files.storage import get_storage_class
from django.conf import settings
from products.models import DigitalProduct
from django.utils import timezone


def get_digital_download_storage():
    """Load storage backend with fallback to default storage"""
    try:
        return get_storage_class(settings.DIGITAL_DOWNLOAD_STORAGE)()
    except Exception:
        from django.core.files.storage import FileSystemStorage
        return FileSystemStorage()


class DigitalDownload(models.Model):
    product = models.OneToOneField(
        DigitalProduct,
        on_delete=models.CASCADE,
        related_name="digital_download",
    )
    file = models.FileField(
        upload_to="digital_downloads/",
        storage=get_digital_download_storage,
        max_length=500,
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} ({self.product.model_number})"

    def is_file_accessible(self):
        """Check if the file is accessible"""
        if not self.file:
            return False
        try:
            # Check if file exists in storage
            return self.file.storage.exists(self.file.name)
        except Exception:
            return False
