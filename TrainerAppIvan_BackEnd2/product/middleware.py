from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from .models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure session exists
        if not hasattr(request, 'session'):
            SessionMiddleware(lambda r: None).process_request(request)

        # Ensure user is attached to request
        if not hasattr(request, 'user'):
            AuthenticationMiddleware(lambda r: None).process_request(request)

        # Get or create cart
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, created = Cart.objects.get_or_create(
                session_id=request.session.session_key,
                user=None
            )

        request.cart = cart
        return self.get_response(request)