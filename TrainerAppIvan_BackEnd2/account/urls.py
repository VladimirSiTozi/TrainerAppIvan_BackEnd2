from django.urls import path, include

from TrainerAppIvan_BackEnd2.account import views

urlpatterns = [
    path('details/', views.AccountDetailView.as_view(), name='account-detail'),
    path('', include([
        path('google_sign_in', views.GoogleView.as_view(), name='google_sign_in')
    ])),
]