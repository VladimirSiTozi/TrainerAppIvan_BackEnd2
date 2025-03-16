from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan


# Create your views here.

class WorkoutPlansListView(ListView):
    model = WorkoutPlan
    template_name = 'programs/training-plans-list.html'
    context_object_name = 'workout_plans'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if self.request.user.email != obj.user.email and self.request.user != obj.trainer.user:
            raise PermissionDenied("You do not have permission to view this workout plan.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout_plans = WorkoutPlan.objects.filter(user=self.request.user).all()
        context['workout_plans'] = workout_plans

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
