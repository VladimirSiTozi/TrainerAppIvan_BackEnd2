from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from TrainerAppIvan_BackEnd2.account.models import AppUser
from TrainerAppIvan_BackEnd2.article.forms import ArticleForm
from TrainerAppIvan_BackEnd2.article.models import Article
from TrainerAppIvan_BackEnd2.mixins import StaffRequiredMixin


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


class CreateArticleView(StaffRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article-create.html'
    success_url = reverse_lazy('articles-home')

    def form_valid(self, form):
        return super().form_valid(form)


class EditArticleView(StaffRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article-edit.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('articles-home')


class DeleteArticleView(StaffRequiredMixin, DeleteView):
    model = Article
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('articles-home')
