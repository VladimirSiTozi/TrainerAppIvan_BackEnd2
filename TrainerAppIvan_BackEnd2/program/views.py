from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView
from django.db.models import Q

from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan, Trainer

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import WorkoutPlan, Period, Day, ExerciseInstance, ExerciseTemplate
from .forms import WorkoutPlanForm, PeriodForm, DayForm, ExerciseInstanceForm
from ..account.models import Profile
from ..mixins import ProfileContextMixin


class WorkoutPlansListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = 'programs/training-plans-list.html'
    context_object_name = 'workout_plans'

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, slug=self.kwargs['slug'])

        # logged-in user
        user = request.user

        # check access
        is_owner = self.profile.user == user
        is_trainer = WorkoutPlan.objects.filter(
            user=self.profile.user,
            trainer__user=user
        ).exists()

        if not user.is_staff and not is_owner and not is_trainer:
            raise PermissionDenied("You do not have permission to view this user's workout plans.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.profile.user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile  # user being viewed
        context['current_user'] = self.request.user  # logged-in user
        context['workout_plans'] = WorkoutPlan.objects.filter(user_id=self.profile.user_id)
        return context


class WorkoutPlanDetailView(DetailView, ProfileContextMixin):
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

        plan = self.object
        context['profile'] = plan.user.profile
        context['current_user'] = self.request.user

        # Load all periods and nested data
        plan_data = []
        for period in plan.periods.all():
            period_data = {
                'period': period.number,
                'duration_weeks': period.duration_weeks,
                'days': []
            }
            for day in period.days.all():
                period_data['days'].append({
                    'day': day.name,
                    'exercises': day.exercises.all()
                })
            plan_data.append(period_data)

        context['plan_data'] = plan_data
        return context


@method_decorator(staff_member_required, name='dispatch')
class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'programs/create_plan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['period_formset'] = PeriodFormSet(self.request.POST, instance=self.object)
        else:
            context['period_formset'] = PeriodFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        period_formset = context['period_formset']

        self.object = form.save(commit=False)
        self.object.trainer = self.request.user.trainer
        self.object.save()

        if period_formset.is_valid():
            periods = period_formset.save(commit=False)
            for period in periods:
                period.workout_plan = self.object
                period.save()

                day_prefix = f'day-{period.id}' if period.id else f'day-new-{period_formset.prefix}'
                day_formset = DayFormSet(
                    self.request.POST,
                    prefix=day_prefix,
                    instance=period
                )

                if day_formset.is_valid():
                    days = day_formset.save(commit=False)
                    for day in days:
                        day.period = period
                        day.save()

                        exercise_prefix = f'exercise-{day.id}' if day.id else f'exercise-new-{day_prefix}'
                        exercise_formset = ExerciseInstanceFormSet(
                            self.request.POST,
                            prefix=exercise_prefix,
                            instance=day
                        )

                        if exercise_formset.is_valid():
                            exercises = exercise_formset.save(commit=False)
                            for exercise in exercises:
                                exercise.day = day
                                exercise.save()
                        else:
                            return self.form_invalid(form)
                else:
                    return self.form_invalid(form)
        else:
            return self.form_invalid(form)

        return redirect(self.object.get_absolute_url())


# Formsets дефиниции
PeriodFormSet = inlineformset_factory(
    WorkoutPlan, Period, form=PeriodForm,
    extra=1, can_delete=True, fields='__all__'
)

DayFormSet = inlineformset_factory(
    Period, Day, form=DayForm,
    extra=1, can_delete=True, fields='__all__'
)

ExerciseInstanceFormSet = inlineformset_factory(
    Day, ExerciseInstance, form=ExerciseInstanceForm,
    extra=1, can_delete=True, fields='__all__'
)