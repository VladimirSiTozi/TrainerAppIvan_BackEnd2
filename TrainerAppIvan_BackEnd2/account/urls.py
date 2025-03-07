from django.urls import path

from TrainerAppIvan_BackEnd2.account import views

urlpatterns = [
    path('details/', views.AccountDetailView.as_view(), name='account-detail'),
]