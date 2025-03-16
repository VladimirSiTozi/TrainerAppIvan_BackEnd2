from django.contrib import admin
from .models import Trainer, WorkoutPlan, Period, Day, ExerciseTemplate, ExerciseInstance


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__profile__first_name', 'user__profile__last_name',)  # Display the related user (AppUser)
    search_fields = ('user__email', 'user__profile__first_name', 'user__profile__last_name')  # Allow searching by user email or username


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'user',)
    search_fields = ('name', 'trainer__user__email', 'user__email')
    list_filter = ('trainer', 'user')


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'number', 'duration_weeks')
    search_fields = ('workout_plan__name',)
    list_filter = ('workout_plan',)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'period','period__workout_plan__trainer', 'period__workout_plan__user', 'number',)
    search_fields = ('period__workout_plan__name',)


@admin.register(ExerciseTemplate)
class ExerciseTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'focus', )
    search_fields = ('name', 'focus')


@admin.register(ExerciseInstance)
class ExerciseInstanceAdmin(admin.ModelAdmin):
    list_display = ('exercise_template', 'day', 'sets', 'reps', 'rest', 'weight', 'tempo')
    search_fields = ('exercise_template__name', 'day__name', 'day__period__workout_plan__name')
    list_filter = ('day',)


