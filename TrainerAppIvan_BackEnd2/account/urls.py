from django.urls import path, include

from TrainerAppIvan_BackEnd2.account import views
from TrainerAppIvan_BackEnd2.program.views import WorkoutPlanDetailView, WorkoutPlansListView

urlpatterns = [
    path('details/', views.AccountDetailView.as_view(), name='account-detail'),
    path('workout-plans', include([
        path('list/', WorkoutPlansListView.as_view(), name='workout-plans-list'),
        path('/<int:pk>/details/', WorkoutPlanDetailView.as_view(), name='workout_plan_details'),
    ])),

    path('', include([
        path('google-sign-in', views.GoogleView.as_view(), name='google_sign_in')
    ])),
]