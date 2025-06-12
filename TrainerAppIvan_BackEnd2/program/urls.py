from django.urls import path

from TrainerAppIvan_BackEnd2.program import views

urlpatterns = [
    path('create-workout/', views.WorkoutPlanCreateView.as_view(), name='create_workout'),
    # path('create/', views.workout_plan_create, name='workout_plan_create'),
    # path('get-period-form/', views.get_period_form, name='get_period_form'),
    # path('get-day-form/', views.get_day_form, name='get_day_form'),
    # path('get-exercise-form/', views.get_exercise_form, name='get_exercise_form'),
    #
    # path('delete-period-form/', views.delete_period_form_row, name='delete_period_form'),
    # path('delete-day-form/', views.delete_day_form_row, name='delete_day_form'),
    # path('delete-exercise-form/', views.delete_exercise_form_row, name='delete_exercise_form'),

    path('create-workout-plan/', views.create_workout_plan, name='create_workout_plan'),
]