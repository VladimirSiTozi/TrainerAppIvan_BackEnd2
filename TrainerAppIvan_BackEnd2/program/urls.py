from django.urls import path

from TrainerAppIvan_BackEnd2.program import views

urlpatterns = [
    path('create-workout/', views.WorkoutPlanCreateView.as_view(), name='create_workout'),
]