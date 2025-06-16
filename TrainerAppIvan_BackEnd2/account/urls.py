from django.urls import path, include

from TrainerAppIvan_BackEnd2.account import views
from TrainerAppIvan_BackEnd2.program.views import WorkoutPlanDetailView, WorkoutPlansListView, ExercisesListView

urlpatterns = [
    path('search/', views.staff_user_search, name='staff-user-search'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('google-sign-in/', views.GoogleView.as_view(), name='google_sign_in'),
    path('register/', views.AccountRegisterView.as_view(), name='register'),
    path('logout/', views.sign_out, name='logout'),
    path('complete-profile/', views.complete_profile, name='complete-profile'),
    path('<slug:slug>/', include([
        path('', views.AccountDetailView.as_view(), name='account-detail'),
        path('adminhub/', include([
            path('', views.AdminHubView.as_view(), name='admin-hub'),
            path('exercises-list/', ExercisesListView.as_view(), name='exercises-list'),
            path('users-list/', views.UsersListView.as_view(), name='users-list'),
        ])),
        path('edit/', views.edit_profile, name='profile-edit'),
        path('workout-plans/', include([
            path('list/', WorkoutPlansListView.as_view(), name='workout-plans-list'),
            path('<int:pk>/details/', WorkoutPlanDetailView.as_view(), name='workout_plan_details'),
        ])),
    ])),
]