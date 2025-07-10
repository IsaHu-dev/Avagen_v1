from django.shortcuts import render


class DisableXFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get('X-Frame-Options'):
            del response['X-Frame-Options']
        return response


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
            return render(request, "404.html", status=404)

        return response
