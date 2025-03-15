from django.urls import path, include

from TrainerAppIvan_BackEnd2.account import views

urlpatterns = [
    path('details/', views.AccountDetailView.as_view(), name='account-detail'),
    path('nutrition', views.AccountNutritionView.as_view(), name='account-nutrition'),
    path('', include([
        path('google-sign-in', views.GoogleView.as_view(), name='google_sign_in')
    ])),
]