from django.urls import path

from TrainerAppIvan_BackEnd2.article import views

urlpatterns = [
    path('', views.ArticleHomeListView.as_view(), name='articles-home'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='articles-detail'),
]