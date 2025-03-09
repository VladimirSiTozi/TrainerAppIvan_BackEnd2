from django.shortcuts import render
from django.views.generic import TemplateView

from TrainerAppIvan_BackEnd2.product.models import Product


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        return context


class CoachingPageView(TemplateView):
    template_name = 'common/coaching.html'


class ArticlePageView():
    template_name = 'common/articles.html'



