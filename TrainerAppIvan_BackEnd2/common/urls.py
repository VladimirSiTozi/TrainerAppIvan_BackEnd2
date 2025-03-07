from django.urls import path

from TrainerAppIvan_BackEnd2.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('coaching/', views.CoachingPageView.as_view(), name='coaching'),
]