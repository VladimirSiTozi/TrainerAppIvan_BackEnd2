from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem


@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    try:
        guest_cart = Cart.objects.get(session_id=request.session.session_key, user=None)
    except Cart.DoesNotExist:
        return

    try:
        user_cart = Cart.objects.get(user=user)
        # Merge logic here...
        for item in guest_cart.items.all():
            try:
                user_item = CartItem.objects.get(cart=user_cart, product=item.product)
                user_item.quantity += item.quantity
                user_item.save()
            except CartItem.DoesNotExist:
                item.cart = user_cart
                item.save()
        guest_cart.delete()
    except Cart.DoesNotExist:
        guest_cart.user = user
        guest_cart.session = None
        guest_cart.save()