from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from TrainerAppIvan_BackEnd2.account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TrainerAppIvan_BackEnd2.common.urls')),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('accounts/', include('TrainerAppIvan_BackEnd2.account.urls')),
    path('shop/', include('TrainerAppIvan_BackEnd2.product.urls')),
    path('articles/', include('TrainerAppIvan_BackEnd2.article.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


