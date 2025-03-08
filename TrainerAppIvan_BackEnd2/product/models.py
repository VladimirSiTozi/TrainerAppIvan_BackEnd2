from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/images/')
    brief_description = models.CharField(max_length=500)
    description = models.TextField()
    will_learn = models.JSONField()  # List of learning points
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchasers = models.ManyToManyField(User, related_name='purchased_products', blank=True)  # Users who purchased
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
