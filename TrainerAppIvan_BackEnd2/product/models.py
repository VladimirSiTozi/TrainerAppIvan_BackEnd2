from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.sessions.models import Session

from TrainerAppIvan_BackEnd2.account.models import AppUser
from TrainerAppIvan_BackEnd2.product.choices import ProductCategoryChoices, ProductTypeChoices


class Product(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=100,
        choices=ProductTypeChoices.CHOICES,
        default=ProductTypeChoices.TRAINING_PLAN
    )
    category = models.CharField(
        max_length=100,
        choices=ProductCategoryChoices.CHOICES,
        default=ProductCategoryChoices.GYM
    )
    image = models.ImageField(upload_to='products/images/')
    brief_description = models.CharField(max_length=500)
    description = models.TextField()
    will_learn = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchasers = models.ManyToManyField(AppUser, related_name='purchased_products', blank=True)  # Users who purchased
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart ({self.user.email})"

    @property
    def total_price(self):
        """Sum of all cart items' prices (with discounts applied)"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product',  # Your existing Product model
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )  # Fixed to 1 (as per your requirement)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product']  # Prevent duplicates
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Cart: {self.cart.user.email})"

    @property
    def total_price(self):
        """Item price after discount (quantity always 1)"""
        return max(0, self.product.price - self.product.discount)
