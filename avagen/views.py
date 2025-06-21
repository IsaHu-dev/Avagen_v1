from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def custom_404(request, exception):
    """
    Custom 404 error handler view.
    Logs the 404 error and renders the custom 404 template.
    """
    # Log the 404 error for monitoring
    logger.warning(
        f"404 error for URL: {request.path} | "
        f"User: {request.user} | "
        f"IP: {request.META.get('REMOTE_ADDR', 'Unknown')} | "
        f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
    )
    
    # Return the custom 404 template
    return render(request, '404.html', status=404) 