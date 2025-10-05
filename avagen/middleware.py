from django.shortcuts import render


class Custom404RedirectMiddleware:
    """
    Intercept 404 responses.

    • By default it renders templates/404.html.
    • Uncomment the redirect() line to send users to the home page instead.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            # --- Option A – show friendly page (default) ---
            # Ensure we don't show debug pages even if DEBUG is True
            from django.conf import settings
            if settings.DEBUG:
                # In debug mode, still show custom 404 to prevent debug pages
                return render(request, "404.html", status=404)
            return render(request, "404.html", status=404)
        return response
