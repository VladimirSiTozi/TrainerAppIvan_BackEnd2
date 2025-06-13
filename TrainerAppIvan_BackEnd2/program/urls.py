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

    path('exercise/<int:pk>/edit/', views.EditExerciseView.as_view(), name='exercise-edit'),
    path('day/<int:pk>/edit', views.EditDayView.as_view(), name='day-edit'),
    path('period/<int:pk>/edit', views.EditPeriodView.as_view(), name='period-edit'),
    path('workout-plan/<int:pk>/edit/', views.EditWorkoutPlanView.as_view(), name='workout-plan-edit'),

    path('day/<int:pk>/exercise/create', views.CreateExerciseTemplateView.as_view(), name='create_exercise'),
    path('period/<int:pk>/day/create', views.CreateDayView.as_view(), name='create-day'),
    path('workplan/<int:pk>period/create', views.CreatePeriodView.as_view(), name='create-period'),

    path('exercise/<int:pk>/delete/', views.DeleteExerciseInstanceView.as_view(), name='delete_exercise'),
    path('day/<int:pk>/delete', views.DeleteDayView.as_view(), name='day-delete'),
    path('period/<int:pk>/delete', views.DeletePeriodView.as_view(), name='period-delete'),
    path('workout-plan/<int:pk>/delete', views.DeleteWorkoutPlanView.as_view(), name='workout-plan-delete'),
]