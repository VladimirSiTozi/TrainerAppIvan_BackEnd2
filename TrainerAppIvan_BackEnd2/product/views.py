from django.shortcuts import render
from django.views.generic import ListView, DetailView

from TrainerAppIvan_BackEnd2.product.models import Product


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

