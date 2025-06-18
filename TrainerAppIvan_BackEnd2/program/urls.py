from django.urls import path, include

from TrainerAppIvan_BackEnd2.program import views

urlpatterns = [
    path('create-workout/', views.WorkoutPlanCreateView.as_view(), name='create_workout'),
    path('create-workout-plan/', views.create_workout_plan, name='create_workout_plan'),

    path('meal/', include([
        path('create/', views.CreateMealView.as_view(), name='create-meal-template'),
        path('<int:pk>/', include([
            path('edit/', views.EditMealView.as_view(), name='edit-meal-template'),
            path('delete/', views.DeleteMealView.as_view(), name='delete-meal-template'),
        ])),

    ])),

    path('exercise-template/', include([
        path('create-new-template/', views.CreateExerciseTemplateView.as_view(), name='create_new_exercise'),
        path('<int:pk>/', include([
            path('edit/', views.EditExerciseTemplateView.as_view(), name='edit_exercise_template'),
            path('delete/', views.DeleteExerciseTemplateView.as_view(), name='delete_exercise_template'),
        ])),
    ])),

    path('exercise/', include([
        path('<int:pk>/', include([
            path('edit/', views.EditExerciseView.as_view(), name='exercise-edit'),
            path('delete/', views.DeleteExerciseInstanceView.as_view(), name='delete_exercise')
        ])),
    ])),

    path('day<int:pk>/', include([
        path('edit/', views.EditDayView.as_view(), name='day-edit'),
        path('exercise/create/', views.CreateExerciseInstanceView.as_view(), name='create_exercise'),
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

    path('nutrition-plan/create/', views.CreateNutritionView.as_view(), name='create-nutrition-plan'),
    path('nutrition-plan/<int:pk>/', include([
        path('edit/', views.EditNutritionView.as_view(), name='nutrition-plan-edit'),
        path('delete/', views.DeleteNutritionView.as_view(), name='nutrition-plan-delete'),
        path('meal/', include([
            path('create/', views.CreateMealInstanceView.as_view(), name='create-meal'),
            path('edit/', views.EditMealInstanceView.as_view(), name='edit-meal'),
            path('delete/', views.DeleteMealInstance.as_view(), name='delete-meal'),
        ])),
    ])),
]