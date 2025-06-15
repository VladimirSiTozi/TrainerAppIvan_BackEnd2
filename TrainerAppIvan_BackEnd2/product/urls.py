from django.urls import path, include

from TrainerAppIvan_BackEnd2.product import views

urlpatterns = [
    path('', views.ProductHomeListView.as_view(), name='shop-home'),
    path('product/', include([
        path('add/', views.CreateProductView.as_view(), name='product-create'),
        path('<int:pk>/', include([
            path('', views.ProductDetailView.as_view(), name='product-detail'),
            path('edit/', views.EditProductView.as_view(), name='product-edit'),
            path('delete/', views.DeleteProductView.as_view(), name='product-delete'),
        ])),

    ])),
    path('cart/', include([
        path('', views.view_cart, name='cart'),
        path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
        path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
        path('success/', views.SuccessPaymentView.as_view(), name='success'),
        path('cancel/', views.CancelPaymentView.as_view(), name='cancel'),
        path('webhooks/stripe/', views.stripe_webhook_view, name='stripe-webhook'),
    ])),
]