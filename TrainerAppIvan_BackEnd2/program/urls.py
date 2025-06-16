from django.urls import path, include

from TrainerAppIvan_BackEnd2.program import views

urlpatterns = [
    path('create-workout/', views.WorkoutPlanCreateView.as_view(), name='create_workout'),
    path('create-workout-plan/', views.create_workout_plan, name='create_workout_plan'),

    path('exercise/<int:pk>/', include([
        path('edit/', views.EditExerciseView.as_view(), name='exercise-edit'),
        path('delete/', views.DeleteExerciseInstanceView.as_view(), name='delete_exercise')
    ])),

    path('day<int:pk>/', include([
        path('edit/', views.EditDayView.as_view(), name='day-edit'),
        path('exercise/create/', views.CreateExerciseTemplateView.as_view(), name='create_exercise'),
        path('delete/', views.DeleteDayView.as_view(), name='day-delete'),
    ])),

    path('period/<int:pk>/', include([
        path('edit/', views.EditPeriodView.as_view(), name='period-edit'),
        path('day/create/', views.CreateDayView.as_view(), name='create-day'),
        path('delete/', views.DeletePeriodView.as_view(), name='period-delete'),
    ])),

    path('workout/<int:pk>/', include([
        path('edit/', views.EditWorkoutPlanView.as_view(), name='workout-plan-edit'),
        path('period/create/', views.CreatePeriodView.as_view(), name='create-period'),
        path('delete/', views.DeleteWorkoutPlanView.as_view(), name='workout-plan-delete'),
    ])),

    # path('day/<int:pk>/edit', views.EditDayView.as_view(), name='day-edit'),
    # path('period/<int:pk>/edit', views.EditPeriodView.as_view(), name='period-edit'),
    # path('workout-plan/<int:pk>/edit/', views.EditWorkoutPlanView.as_view(), name='workout-plan-edit'),

    # path('day/<int:pk>/exercise/create', views.CreateExerciseTemplateView.as_view(), name='create_exercise'),
    # path('period/<int:pk>/day/create', views.CreateDayView.as_view(), name='create-day'),
    # path('workplan/<int:pk>period/create', views.CreatePeriodView.as_view(), name='create-period'),

    # path('exercise/<int:pk>/delete/', views.DeleteExerciseInstanceView.as_view(), name='delete_exercise'),
    # path('day/<int:pk>/delete', views.DeleteDayView.as_view(), name='day-delete'),
    # path('period/<int:pk>/delete', views.DeletePeriodView.as_view(), name='period-delete'),
    # path('workout-plan/<int:pk>/delete', views.DeleteWorkoutPlanView.as_view(), name='workout-plan-delete'),
]