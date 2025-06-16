from django.urls import path, include

from TrainerAppIvan_BackEnd2.article import views

urlpatterns = [
    path('', views.ArticleHomeListView.as_view(), name='articles-home'),
    path('create-article/', views.CreateArticleView.as_view(), name='create-article'),
    path('<int:pk>/', include([
        path('', views.ArticleDetailView.as_view(), name='article-detail'),
        path('edit/', views.EditArticleView.as_view(), name='article-edit'),
        path('delete/', views.DeleteArticleView.as_view(), name='article-delete'),
    ])),
]