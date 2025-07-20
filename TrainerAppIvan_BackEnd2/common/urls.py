from django.urls import path, include

from TrainerAppIvan_BackEnd2.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('coaching/', views.CoachingPageView.as_view(), name='coaching'),
    path('contact-me/', views.ContactMeView.as_view(), name='contact-me'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('apply/', include([
        path('', views.ApplyView.as_view(), name='apply'),
        path('application-form/', views.ApplicationFormView.as_view(), name='application-form'),
    ])),
    path('business-card/', views.BusinessCardView.as_view(), name='business-card'),
    path('verify-email/', views.VerifyEmailMessageView.as_view(), name='verify-email-message'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]