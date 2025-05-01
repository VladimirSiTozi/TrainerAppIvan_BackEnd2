import stripe
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from TrainerAppIvan_BackEnd2.product.models import Product, CartItem, Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductHomeListView(ListView):
    model = Product
    template_name = 'product/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.only('id', 'name', 'brief_description', 'image')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.cart

    # Check if product is already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} е добавен към количката!")
    return redirect('shop-home')


def remove_from_cart(request, cart_item_id):
    # product = get_object_or_404(Product, id=product_id)
    cart = request.cart
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    print(cart_item)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=cart_item)
        cart_item.delete()
        messages.success(request, f"{cart_item.name} е премахнат от количката!")
    except CartItem.DoesNotExist:
        messages.error(request, "Продуктът не е намерен в количката!")

    return redirect('cart')


def view_cart(request):
    cart = request.cart
    cart_items = cart.items.all()

    context = {'cart': cart,
               'cart_items': cart_items,
               'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
               }

    return render(request, 'common/cart.html', {'cart_items': cart_items, 'cart': cart})


@login_required
def checkout(request):
    cart = request.cart

    if cart.items.count() == 0:
        messages.error(request, "Количката ви е празна!")
        return redirect('view_cart')

    # Transfer cart to user if it was a guest cart
    if not cart.user:
        cart.user = request.user
        cart.session = None
        cart.save()

    # Proceed with checkout logic
    return render(request, 'cart/checkout.html', {'cart': cart})


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        # Get the user's cart
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        # Create Stripe line items
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.total_price * 100),  # Convert to cents
                },
                'quantity': item.quantity,
            })
            print(line_items)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.SITE_URL + 'success/',
                cancel_url=settings.SITE_URL + 'cancel/',
            )
            return JsonResponse({'url': checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


class SuccessPaymentView(TemplateView):
    template_name = 'common/success-payment.html'


class CancelPaymentView(TemplateView):
    template_name = 'common/cancel-payment.html'
