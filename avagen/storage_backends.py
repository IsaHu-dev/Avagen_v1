from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings


class GoogleCloudZipStorage(GoogleCloudStorage):
    """
    Custom Google Cloud Storage backend for Digital Downloads.
    Ensures credentials are passed from settings.GS_CREDENTIALS.
    """

    bucket_name = settings.GS_BUCKET_NAME
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        # Inject credentials if available
        if settings.GS_CREDENTIALS:
            kwargs["credentials"] = settings.GS_CREDENTIALS
        super().__init__(*args, **kwargs)
