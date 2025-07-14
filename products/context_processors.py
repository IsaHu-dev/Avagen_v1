# products/context_processors.py

from .models import Category


def categories_context(request):
    """Adds all categories to the context for global use (e.g. navbar)."""
    return {
        'categories': Category.objects.all()
    }
