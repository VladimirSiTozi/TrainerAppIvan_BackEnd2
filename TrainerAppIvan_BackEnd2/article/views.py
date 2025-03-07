from django.shortcuts import render
from django.views.generic import ListView, DetailView

from TrainerAppIvan_BackEnd2.article.models import Article


# Create your views here.

class ArticleHomeListView(ListView):
    model = Article
    template_name = "article/articles.html"
    context_object_name = "articles"  # Variable name for template

    def get_queryset(self):
        return Article.objects.only("id", "name", "brief_description", "image1")  # Fetch only required fields


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article/article-details.html"
    context_object_name = "article"  # Variable name for template

