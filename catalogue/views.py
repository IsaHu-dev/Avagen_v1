from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, FileResponse
from products.models import Product
from .models import DigitalDownload

def catalogue_view(request):
    """
    View to display the catalogue of available products
    """
    products = Product.objects.all().order_by('-rating') 
    context = {
        'products': products,
    }
    return render(request, 'catalogue/catalogue.html', context)

def download_file(request, product_id):
    """
    View to handle digital file downloads
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product has a digital download
    try:
        digital_download = DigitalDownload.objects.get(product=product)
    except DigitalDownload.DoesNotExist:
        raise Http404("No digital download found for this product")
    
    # Check if user has purchased the product
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    # TODO: Add purchase verification logic here
    
    # Return the file for download
    return FileResponse(digital_download.file, as_attachment=True)




