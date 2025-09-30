from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import DigitalProduct
from checkout.models import Order
from .models import DigitalDownload


def catalogue(request):
    """
    View to display the catalogue of available products
    """
    products = DigitalProduct.objects.filter(status="published").order_by(
        "-date_created"
    )
    context = {
        "products": products,
    }
    return render(request, "catalogue/catalogue.html", context)


@login_required
def download_file(request, product_id):
    """Handle digital file downloads for purchased products"""
    try:
        product = get_object_or_404(DigitalProduct, id=product_id)
        digital_download = get_object_or_404(DigitalDownload, product=product)
        
        # Check if user purchased this product
        if not Order.objects.filter(
            user=request.user, stripe_pid__isnull=False, lineitems__product=product
        ).exists():
            messages.error(request, "You need to purchase this product to download it.")
            return redirect("products")
        
        # Check if file is accessible
        if not digital_download.file or not digital_download.is_file_accessible():
            messages.error(request, f"Download file for '{product.name}' is not available.")
            return redirect("products")
        
        return FileResponse(digital_download.file, as_attachment=True)
        
    except Exception as e:
        messages.error(request, "Download error. Please try again or contact support.")
        return redirect("products")
