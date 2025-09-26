from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
import os
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    help = 'Upload media files to Cloudinary'

    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT)
        
        if not media_dir.exists():
            self.stdout.write(self.style.WARNING('Media directory does not exist'))
            return

        uploaded_count = 0
        
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                # Convert Windows backslashes to forward slashes for Cloudinary
                relative_path = relative_path.replace('\\', '/')
                
                try:
                    # Skip if file already exists in Cloudinary
                    if default_storage.exists(relative_path):
                        self.stdout.write(f'Skipping {relative_path} (already exists)')
                        continue
                except Exception:
                    # If we can't check existence, try to upload anyway
                    pass
                
                try:
                    with open(file_path, 'rb') as f:
                        default_storage.save(relative_path, f)
                    uploaded_count += 1
                    self.stdout.write(f'Uploaded: {relative_path}')
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to upload {relative_path}: {e}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully uploaded {uploaded_count} files to Cloudinary')
        )