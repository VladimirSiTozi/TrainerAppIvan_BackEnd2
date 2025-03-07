from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'common/home.html'


class CoachingPageView(TemplateView):
    template_name = 'common/coaching.html'


class ArticlePageView():
    template_name = 'common/articles.html'



