import stripe
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from TrainerAppIvan_BackEnd2.mixins import StaffRequiredMixin
from TrainerAppIvan_BackEnd2.product.forms import ProductForm
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
    template_name = 'product/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']

        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).order_by('-created_at')[:3]
        return context


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
        if product.type == 'training program':
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} е добавен към количката!")
    return redirect('shop-home')


@require_POST
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.cart

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f"{product.name} е премахнат от количката!")
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

    return render(request, 'common/cart.html', context)


# ????????????
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
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return JsonResponse({'error': 'Your cart is empty'}, status=400)

        product_ids = []
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),  # Use price, not total_price
                },
                'quantity': item.quantity,
            })
            product_ids.append(str(item.product.id))

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                metadata={
                    "product_ids": ",".join(product_ids),
                },
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),  # Use reverse()
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )
            return JsonResponse({'url': checkout_session.url})
        except stripe.error.CardError as e:
            # Handle specific card errors (e.g., insufficient funds)
            return JsonResponse({'error': e.user_message}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def stripe_webhook_view(request):
    if request.method != 'POST':
        return HttpResponse(status=400)

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'):
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_ids = session["metadata"]["product_ids"].split(",")

        # Load products
        products = []
        for product_id in product_ids:
            product = get_object_or_404(Product, id=product_id)
            products.append(product)

        product_names = ", ".join(product.name for product in products)

        # HTML block for products
        product_html = ""
        for product in products:
            image_url = request.build_absolute_uri(product.image.url) if product.image else ""
            product_html += f"""
                <div style="margin-bottom: 20px; padding: 10px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 5px 0;">{product.name} personal training plan</h3>
                    <p style="margin: 0;">Price: ${product.price}</p>
                    {"<img src='" + image_url + "' alt='" + product.name + "' style='width: 200px; margin-top: 10px;' />" if image_url else ""}
                </div>
            """

        # ===== Customer Email =====
        customer_subject = "Thank You for Your Purchase! 🎉"
        customer_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 10px;">
              <h1 style="color: #4CAF50; text-align: center;">Thank You for Your Purchase!</h1>
              <p>Hi {customer_email},</p> 
              <p>I'm Ivan The Bear, and I'll be your personal trainer!</p> 
              <p>I've just received your order and will begin creating a personalized training plan for you. This will take a few business days to complete.</p> 
              <p>Before I can get started, please fill out the form below so that I can tailor the plan specifically to your goals and needs.</p> 
              <p>TODO: Application Form Link here</p>
              <p>Looking forward to working with you!</p>
              {product_html}
              <p>If you have any questions, just reply to this email.</p>
              <p style="color: #888;">– Your Team</p>
            </div>
          </body>
        </html>
        """
        customer_plain = strip_tags(customer_html)

        customer_email_obj = EmailMultiAlternatives(
            subject=customer_subject,
            body=customer_plain,
            from_email=settings.EMAIL_HOST_USER,
            to=[customer_email],
        )
        customer_email_obj.attach_alternative(customer_html, "text/html")
        customer_email_obj.send()

        # ===== Host/Admin Email =====
        host_subject = f"New Payment: Customer {customer_email} purchased {product_names}"
        host_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #fff; padding: 20px;">
            <h2 style="color: #333;">New Payment Received</h2>
            <p><strong>Customer email:</strong> {customer_email}</p>
            <p><strong>Products:</strong></p>
            {product_html}
            <p>Check the admin panel for more details.</p>
          </body>
        </html>
        """
        host_plain = strip_tags(host_html)

        host_email_obj = EmailMultiAlternatives(
            subject=host_subject,
            body=host_plain,
            from_email=settings.EMAIL_HOST_USER,
            to=['ivanthebear.contact@gmail.com'],
        )
        host_email_obj.attach_alternative(host_html, "text/html")
        host_email_obj.send()

    return HttpResponse(status=200)


@method_decorator(login_required, name='dispatch')
class SuccessPaymentView(TemplateView):
    template_name = 'common/success-payment.html'


@method_decorator(login_required, name='dispatch')
class CancelPaymentView(TemplateView):
    template_name = 'common/cancel-payment.html'


# Products Create, Edit, Delete
class CreateProductView(StaffRequiredMixin, CreateView):
    model = Product
    template_name = 'product/product-create.html'
    form_class = ProductForm
    success_url = reverse_lazy('shop-home')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.active = self.request.user
        form.save()
        return super().form_valid(form)


class EditProductView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product-edit.html'
    success_url = reverse_lazy('shop-home')

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteProductView(StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('shop-home')

    def get(self, request, *args, **kwargs):
        return redirect('product-edit', pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductsListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = 'product/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('name')
