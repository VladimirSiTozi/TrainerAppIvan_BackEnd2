from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from TrainerAppIvan_BackEnd2.product.models import Product, CartItem, Cart


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
    return render(request, 'common/cart.html', {'cart_items': cart_items, 'cart': cart})


# @login_required()
# def checkout_overview(request):
#     return render(request, 'common/checkout-overview.html')


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

