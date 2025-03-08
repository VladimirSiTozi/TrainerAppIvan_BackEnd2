from django.contrib import admin

from TrainerAppIvan_BackEnd2.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    list_filter = ('name', 'price', 'image')
    search_fields = ('name', 'price', 'image')

