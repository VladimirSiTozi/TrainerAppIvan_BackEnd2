from django.urls import path, include

from TrainerAppIvan_BackEnd2.product import views

urlpatterns = [
    path('', views.ProductHomeListView.as_view(), name='shop-home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail', ),
    path('cart/', include([
        path('', views.view_cart, name='cart'),
        path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
        path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
        path('success/', views.SuccessPaymentView.as_view(), name='success'),
        path('cancel/', views.CancelPaymentView.as_view(), name='cancel'),
    ])),
]