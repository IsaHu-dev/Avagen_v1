from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings

class GoogleCloudZipStorage(GoogleCloudStorage):
    bucket_name = settings.GS_BUCKET_NAME
    file_overwrite = False
