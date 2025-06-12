import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView, CreateView
from django.db.models import Q

from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan, Trainer

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import WorkoutPlan, Period, Day, ExerciseInstance, ExerciseTemplate
from .forms import WorkoutPlanForm, PeriodForm, DayForm, ExerciseInstanceForm
from ..account.models import Profile, AppUser
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


# @method_decorator(staff_member_required, name='dispatch')
# class WorkoutPlanCreateView(CreateView):
#     model = WorkoutPlan
#     form_class = WorkoutPlanForm
#     template_name = 'programs/create_plan2.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['period_formset'] = PeriodFormSet(self.request.POST, instance=self.object)
#             # Add empty formsets for POST too (needed for validation)
#             context['day_formset'] = DayFormSet(prefix='day__prefix__')
#             context['exercise_formset'] = ExerciseInstanceFormSet(prefix='exercise__prefix__')
#         else:
#             context['period_formset'] = PeriodFormSet(instance=self.object)
#             # Add empty formsets for template rendering
#             context['day_formset'] = DayFormSet(prefix='day__prefix__')
#             context['exercise_formset'] = ExerciseInstanceFormSet(prefix='exercise__prefix__')
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         period_formset = context['period_formset']
#
#         self.object = form.save(commit=False)
#         self.object.trainer = self.request.user.trainer
#         self.object.save()
#
#         if period_formset.is_valid():
#             periods = period_formset.save(commit=False)
#             for period in periods:
#                 period.workout_plan = self.object
#                 period.save()
#
#                 day_prefix = f'day-{period.id}' if period.id else f'day-new-{period_formset.prefix}'
#                 day_formset = DayFormSet(
#                     self.request.POST,
#                     prefix=day_prefix,
#                     instance=period
#                 )
#
#                 if day_formset.is_valid():
#                     days = day_formset.save(commit=False)
#                     for day in days:
#                         day.period = period
#                         day.save()
#
#                         exercise_prefix = f'exercise-{day.id}' if day.id else f'exercise-new-{day_prefix}'
#                         exercise_formset = ExerciseInstanceFormSet(
#                             self.request.POST,
#                             prefix=exercise_prefix,
#                             instance=day
#                         )
#
#                         if exercise_formset.is_valid():
#                             exercises = exercise_formset.save(commit=False)
#                             for exercise in exercises:
#                                 exercise.day = day
#                                 exercise.save()
#                         else:
#                             return self.form_invalid(form)
#                 else:
#                     return self.form_invalid(form)
#         else:
#             return self.form_invalid(form)
#
#         return redirect(self.object.get_absolute_url())

@method_decorator(staff_member_required, name='dispatch')
class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'programs/create_plan2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['period_formset'] = PeriodFormSet(self.request.POST, prefix='periods')
        else:
            context['period_formset'] = PeriodFormSet(prefix='periods')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        period_formset = context['period_formset']

        if not period_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save(commit=False)
        self.object.trainer = self.request.user.trainer_profile
        self.object.save()

        periods = period_formset.save(commit=False)
        for period in periods:
            period.workout_plan = self.object
            period.save()

            day_prefix = f'day-{period.pk}'
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

                    exercise_prefix = f'exercise-{day.pk}'
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


# # Create Plan 3
# @staff_member_required
# def workout_plan_create(request):
#     if request.method == 'POST':
#         plan_form = WorkoutPlanForm(request.POST)
#         if plan_form.is_valid():
#             plan = plan_form.save(commit=False)
#             plan.trainer = request.user.trainer_profile
#             plan.save()
#
#             # 🧩 Примерно търсим period_0_*, period_1_*, etc
#             i = 0
#             while f'period_{i}_number' in request.POST:
#                 period = Period.objects.create(
#                     workout_plan=plan,
#                     number=request.POST.get(f'period_{i}_number'),
#                     duration_weeks=request.POST.get(f'period_{i}_duration_weeks'),
#                 )
#
#                 # 🔁 Във всеки период, обхождаме дните
#                 j = 0
#                 while f'period_{i}_day_{j}_name' in request.POST:
#                     Day.objects.create(
#                         period=period,
#                         name=request.POST.get(f'period_{i}_day_{j}_name'),
#                     )
#                     j += 1
#
#                 i += 1
#
#             return redirect('workout_plan_detail', pk=plan.pk)
#     else:
#         plan_form = WorkoutPlanForm()
#
#     return render(request, 'programs/create_plan3.html', {
#         'plan_form': plan_form,
#     })
#
#
#
# def get_period_form(request):
#     form = PeriodForm()
#     html = render_to_string('programs/partials/period_form.html', {'form': form})
#     return HttpResponse(html)
#
#
# def get_day_form(request):
#     form = DayForm()
#     html = render_to_string('programs/partials/day_form.html', {'form': form})
#     return HttpResponse(html)
#
#
# def get_exercise_form(request):
#     form = ExerciseInstanceForm()
#     html = render_to_string('programs/partials/exercise_form.html', {'form': form})
#     return HttpResponse(html)
#
# @require_http_methods(["DELETE"])
# def delete_period_form_row(request):
#     return HttpResponse('')
#
# @require_http_methods(["DELETE"])
# def delete_day_form_row(request):
#     return HttpResponse('')
#
# @require_http_methods(["DELETE"])
# def delete_exercise_form_row(request):
#     return HttpResponse('')




# views.py


@csrf_exempt
def create_workout_plan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        print(data)

        user = AppUser.objects.get(id=data['user'])
        trainer = Trainer.objects.get(user=request.user)  # или подай от фронта

        plan = WorkoutPlan.objects.create(
            user=user,
            trainer=trainer,
            name=data['name'],
            description=data.get('description', '')
        )
        print(plan)

        for period_data in data.get('periods', []):
            period = Period.objects.create(
                workout_plan=plan,
                number=period_data['number'],
                duration_weeks=period_data['duration_weeks']
            )

            for day_index, day_data in enumerate(period_data.get('days', []), start=1):
                day = Day.objects.create(
                    period=period,
                    number=day_index,
                    name=day_data.get('name', '')
                )

                for exercise_data in day_data.get('exercises', []):
                    # Намери шаблона (или създай ако липсва)
                    exercise_name = exercise_data.get('exercise')
                    exercise_template, _ = ExerciseTemplate.objects.get_or_create(name=exercise_name)

                    ExerciseInstance.objects.create(
                        day=day,
                        exercise_template=exercise_template,
                        sets=int(exercise_data.get('sets', 0) or 0),
                        reps=exercise_data.get('reps', ''),
                        rest=exercise_data.get('rest', ''),
                        progression=exercise_data.get('progression', ''),
                        aim=exercise_data.get('aim', ''),
                        weight=exercise_data.get('weight', ''),
                        tempo=exercise_data.get('tempo', ''),
                    )

        return JsonResponse({'status': 'success', 'message': 'Workout plan created'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
