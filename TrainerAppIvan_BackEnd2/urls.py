from django.contrib import admin
from django.urls import path, include

from TrainerAppIvan_BackEnd2.account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('register/', views.AccountRegisterView.as_view(), name='register'),
    path('', include('TrainerAppIvan_BackEnd2.common.urls')),
    path('account/', include('TrainerAppIvan_BackEnd2.account.urls')),
    path('cart/', include('TrainerAppIvan_BackEnd2.cart.urls')),
    path('product/', include('TrainerAppIvan_BackEnd2.product.urls')),
]

