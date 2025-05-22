import os
from django.core.management.base import BaseCommand
from products.models import Product

# Base URL for Cloudinary where images are assumed to be hosted
CLOUDINARY_BASE = "https://res.cloudinary.com/dalw18spe/image/upload/v1/"

class Command(BaseCommand):
    # Help text shown when running `python manage.py help <command>`
    help = "Update product.image_url from image file paths (assuming they've been uploaded to Cloudinary)"

    def handle(self, *args, **options):
        updated = 0  # Counter to track how many products were updated

        # Iterate over all products in the database
        for product in Product.objects.all():
            # Only update if the product has an image but no image_url
            if product.image and not product.image_url:
                # Extract the filename from the image path
                filename = os.path.basename(product.image.name)
                
                # Construct the Cloudinary URL using the filename
                cloudinary_url = CLOUDINARY_BASE + filename

                # Assign the new URL to the product and save it
                product.image_url = cloudinary_url
                product.save(update_fields=["image_url"])

                # Print a success message for this product
                self.stdout.write(self.style.SUCCESS(f"Updated {product.name}: {cloudinary_url}"))
                updated += 1

        # Final success message showing how many products were updated
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done. {updated} products updated."))
