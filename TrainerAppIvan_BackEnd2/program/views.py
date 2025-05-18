from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.db.models import Q

from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan


# Create your views here.

class WorkoutPlansListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = 'programs/training-plans-list.html'
    context_object_name = 'workout_plans'

    def get_queryset(self):
        # Only show workout plans belonging to the current user
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def get_queryset(self):
            return WorkoutPlan.objects.filter(
                Q(user=self.request.user) |
                Q(trainer__user=self.request.user)
            ).distinct()
        return context


class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    template_name = 'programs/training-plan.html'
    context_object_name = 'workout_plan'

    def get_object(self, queryset=None):
        # Fetch the workout plan object
        obj = super().get_object(queryset=queryset)

        # Check if the logged-in user is the assigned user or the trainer
        if self.request.user.email != obj.user.email and self.request.user != obj.trainer.user:
            raise PermissionDenied("You do not have permission to view this workout plan.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        periods = self.object.periods.all()

        plan_data = []
        for period in periods:
            period_data = {
                'period': period.number,
                'duration_weeks': period.duration_weeks,
                'days': []
            }

            for day in period.days.all():
                dat_data = {
                    'day': day.name,
                    'exercises': day.exercises.all()
                }
                period_data['days'].append(dat_data)
            plan_data.append(period_data)

        context['plan_data'] = plan_data
        return context
