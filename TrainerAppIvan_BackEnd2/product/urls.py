from django.urls import path

from TrainerAppIvan_BackEnd2.product import views

urlpatterns = [
    path('', views.ProductHomeListView.as_view(), name='shop-home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail', )
]