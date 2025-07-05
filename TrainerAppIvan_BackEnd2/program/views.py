import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan, Trainer, NutritionPlan, MealInstance, Meal, Supplement, \
    SupplementInstance, RecoveryPlan

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import WorkoutPlan, Period, Day, ExerciseInstance, ExerciseTemplate
from .forms import WorkoutPlanForm, PeriodForm, DayForm, ExerciseInstanceForm, ExerciseTemplateForm, NutritionPlanForm, \
    MealInstanceForm, MealForm, SupplementForm, SupplementInstanceForm, RecoveryPlanForm
from ..account.models import Profile, AppUser
from ..mixins import ProfileContextMixin, StaffRequiredMixin


# WorkoutPlan
# @method_decorator(login_required, name='dispatch')
class WorkoutPlansListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = 'programs/workout-plan-list.html'
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


# @method_decorator(login_required, name='dispatch')
class WorkoutPlanDetailView(LoginRequiredMixin, DetailView, ProfileContextMixin):
    model = WorkoutPlan
    template_name = 'programs/workout-plan-details.html'
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
                'pk': period.pk,
                'period': period.number,
                'duration_weeks': period.duration_weeks,
                'days': []
            }
            for day in period.days.all().order_by('number'):
                period_data['days'].append({
                    'pk': day.pk,
                    'day': day.name,
                    'exercises': day.exercises.all().order_by('order'),
                })
            plan_data.append(period_data)

        context['plan_data'] = plan_data
        return context


class WorkoutPlanCreateView(StaffRequiredMixin, CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'programs/workout-plan-create.html'


@csrf_exempt
@staff_member_required
def create_workout_plan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)

        user = AppUser.objects.get(id=data['user'])
        trainer = Trainer.objects.get(user=request.user)  # или подай от фронта

        plan = WorkoutPlan.objects.create(
            user=user,
            trainer=trainer,
            name=data['name'],
            description=data.get('description', '')
        )

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

        # return redirect('workout_plan_details', pk=plan.pk, slug=plan.user.profile.slug)

        return JsonResponse({
            'status': 'success',
            'message': 'Workout plan created',
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class EditWorkoutPlanView(StaffRequiredMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'programs/workout-plan-edit.html'
    context_object_name = 'workout_plan'

    def get_success_url(self):
        workout_plan = self.object
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class DeleteWorkoutPlanView(StaffRequiredMixin, DeleteView):
    model = WorkoutPlan
    context_object_name = 'workout_plan'

    def get_success_url(self):
        profile = self.object.user.profile
        return reverse_lazy('account-detail', kwargs={'slug': profile.slug})


# Days
class CreateDayView(StaffRequiredMixin, CreateView):
    model = Day
    form_class = DayForm
    template_name = 'programs/day-add.html'

    def dispatch(self, request, *args, **kwargs):
        self.period = get_object_or_404(Period, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.period = self.period
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period'] = self.period
        return context

    def get_success_url(self):
        workout_plan = self.object.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class EditDayView(StaffRequiredMixin, UpdateView):
    model = Day
    form_class = DayForm
    template_name = 'programs/day-edit.html'
    context_object_name = 'day'

    def get_success_url(self):
        workout_plan = self.object.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class DeleteDayView(StaffRequiredMixin, DeleteView):
    model = Day
    context_object_name = 'day'

    def get_success_url(self):
        workout_plan = self.object.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


# Period
class CreatePeriodView(StaffRequiredMixin, CreateView):
    model = Period
    form_class = PeriodForm
    template_name = 'programs/period-add.html'
    context_object_name = 'period'

    def dispatch(self, request, *args, **kwargs):
        self.workout_plan = get_object_or_404(WorkoutPlan, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.workout_plan = self.workout_plan
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_plan'] = self.workout_plan
        return context

    def get_success_url(self):
        workout_plan = self.object.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class EditPeriodView(StaffRequiredMixin, UpdateView):
    model = Period
    form_class = PeriodForm
    template_name = 'programs/period-edit.html'
    context_object_name = 'period'

    def get_success_url(self):
        workout_plan = self.object.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class DeletePeriodView(StaffRequiredMixin, DeleteView):
    model = Period
    context_object_name = 'period'

    def get_success_url(self):
        workout_plan = self.object.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


# Exercise
class ExerciseTemplateDetailsView(LoginRequiredMixin, DetailView):
    model = ExerciseTemplate
    context_object_name = 'exercise'
    template_name = 'programs/exercise-template-details.html'


class CreateExerciseTemplateView(StaffRequiredMixin, CreateView):
    model = ExerciseTemplate
    form_class = ExerciseTemplateForm
    template_name = 'programs/exercise-template-create.html'

    def get_success_url(self):
        return reverse_lazy('exercises-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class CreateExerciseInstanceView(StaffRequiredMixin, CreateView):
    model = ExerciseTemplate
    form_class = ExerciseInstanceForm
    template_name = 'programs/exercise-add.html'
    context_object_name = 'exercise'

    def dispatch(self, request, *args, **kwargs):
        self.day = get_object_or_404(Day, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.day = self.day
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day'] = self.day
        return context

    def get_success_url(self):
        workout_plan = self.object.day.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class EditExerciseTemplateView(StaffRequiredMixin, UpdateView):
    model = ExerciseTemplate
    form_class = ExerciseTemplateForm
    template_name = 'programs/exercise-template-edit.html'
    context_object_name = 'exercise'

    def get_success_url(self):
        return reverse_lazy('exercises-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class EditExerciseView(StaffRequiredMixin, UpdateView):
    model = ExerciseInstance
    form_class = ExerciseInstanceForm
    template_name = 'programs/exercise-edit.html'
    context_object_name = 'exercise'

    def get_success_url(self):
        workout_plan = self.object.day.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


class ExercisesListView(StaffRequiredMixin, ListView):
    model = ExerciseTemplate
    template_name = 'account/../../templates/programs/exercise-list-admin.html'
    context_object_name = 'exercises'
    queryset = ExerciseTemplate.objects.order_by('name')


class DeleteExerciseTemplateView(StaffRequiredMixin, DeleteView):
    model = ExerciseTemplate
    context_object_name = 'exercise'

    def get_success_url(self):
        return reverse_lazy('exercises-list', kwargs={'slug': self.request.user.profile.slug})


class DeleteExerciseInstanceView(StaffRequiredMixin, DeleteView):
    model = ExerciseInstance
    context_object_name = 'exercise'

    def get_success_url(self):
        workout_plan = self.object.day.period.workout_plan
        return reverse_lazy('workout_plan_details',
                            kwargs={'pk': workout_plan.id, 'slug': workout_plan.user.profile.slug})


# Nutrition Plan
class AllWorkoutPlanListView(StaffRequiredMixin, ListView):
    model = WorkoutPlan
    template_name = 'programs/workouts-list-admin.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return WorkoutPlan.objects.all().order_by('id')


class AllNutritionPlanListView(StaffRequiredMixin, ListView):
    model = NutritionPlan
    template_name = 'programs/nutrition/nutrition-plans-list-admin.html'
    context_object_name = 'nutrition_plans'

    def get_queryset(self):
        return NutritionPlan.objects.all().order_by('id')


# @method_decorator(login_required, name='dispatch')
class NutritionPlansListView(LoginRequiredMixin, ListView):
    model = NutritionPlan
    template_name = 'programs/nutrition/nutrition-plans-list.html'
    context_object_name = 'nutrition_plans'

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, slug=self.kwargs['slug'])

        # logged-in user
        user = request.user

        # check access
        is_owner = self.profile.user == user

        if not user.is_staff and not is_owner:
            raise PermissionDenied("You do not have permission to view this user's workout plans.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return NutritionPlan.objects.filter(user=self.profile.user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile  # user being viewed
        context['current_user'] = self.request.user  # logged-in user
        return context


class NutritionPlanDetailView(LoginRequiredMixin, DetailView):
    model = NutritionPlan
    template_name = 'programs/nutrition/nutrition-details.html'
    context_object_name = 'nutrition_plan'

    def get_queryset(self):
        # Optionally restrict staff access to users they manage
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nutrition_plan = self.object
        context['profile'] = nutrition_plan.user.profile
        context['meals'] = nutrition_plan.meal_instances.all()
        context['breakfast'] = nutrition_plan.meal_instances.filter(time_of_day='Breakfast')
        context['morning_snack'] = nutrition_plan.meal_instances.filter(time_of_day='Morning Snack')
        context['lunch'] = nutrition_plan.meal_instances.filter(time_of_day='Lunch')
        context['afternoon_snack'] = nutrition_plan.meal_instances.filter(time_of_day='Afternoon Snack')
        context['dinner'] = nutrition_plan.meal_instances.filter(time_of_day='Dinner')
        context['evening_snack'] = nutrition_plan.meal_instances.filter(time_of_day='Evening Snack')

        return context


class CreateNutritionView(StaffRequiredMixin, CreateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'programs/nutrition/nutrition-create.html'
    context_object_name = 'nutrition_plan'

    def get_success_url(self):
        nutrition_plan = self.object
        return reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)


class EditNutritionView(StaffRequiredMixin, UpdateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'programs/nutrition/nutrition-edit.html'
    context_object_name = 'nutrition_plan'

    def get_success_url(self):
        nutrition_plan = self.object
        print(nutrition_plan.user.profile.slug)
        return reverse_lazy('nutrition-plan-details', kwargs={'slug': nutrition_plan.user.profile.slug,
                                                              'pk': nutrition_plan.pk})

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteNutritionView(StaffRequiredMixin, DeleteView):
    model = NutritionPlan
    context_object_name = 'nutrition_plan'

    def get_success_url(self):
        profile = self.object.user.profile
        return reverse_lazy('account-detail', kwargs={'slug': profile.slug})


# Meal
class CreateMealInstanceView(StaffRequiredMixin, CreateView):
    model = MealInstance
    form_class = MealInstanceForm
    template_name = 'programs/nutrition/meal-instance-create.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the nutrition plan from the URL
        self.nutrition_plan = get_object_or_404(NutritionPlan, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the nutrition plan automatically before saving
        form.instance.nutrition_plan = self.nutrition_plan
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nutrition_plan'] = self.nutrition_plan
        return context

    def get_success_url(self):
        profile = self.object.nutrition_plan.user.profile
        return reverse_lazy('nutrition-plan-details', kwargs={'slug': profile.slug, 'pk': self.nutrition_plan.pk})


class EditMealInstanceView(StaffRequiredMixin, UpdateView):
    model = MealInstance
    form_class = MealInstanceForm
    template_name = 'programs/nutrition/meal-instance-edit.html'
    context_object_name = 'meal_instance'

    def get_success_url(self):
        nutrition_plan = self.object.nutrition_plan
        return reverse_lazy('nutrition-plan-details',
                            kwargs={'pk': nutrition_plan.id, 'slug': nutrition_plan.user.profile.slug})


class DeleteMealInstance(StaffRequiredMixin, DeleteView):
    model = MealInstance
    context_object_name = 'meal_instance'

    def get_success_url(self):
        nutrition_plan = self.object.nutrition_plan
        return reverse_lazy('nutrition-plan-details',
                            kwargs={'pk': nutrition_plan.id, 'slug': nutrition_plan.user.profile.slug})


class CreateMealView(StaffRequiredMixin, CreateView):
    model = Meal
    form_class = MealForm
    template_name = 'programs/nutrition/meal-create.html'

    def get_success_url(self):
        return reverse_lazy('meals-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class EditMealView(StaffRequiredMixin, UpdateView):
    model = Meal
    form_class = MealForm
    template_name = 'programs/nutrition/meal-edit.html'
    context_object_name = 'meal'

    def get_success_url(self):
        return reverse_lazy('meals-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteMealView(StaffRequiredMixin, DeleteView):
    model = Meal
    context_object_name = 'meal'

    def get_success_url(self):
        return reverse_lazy('meals-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class MealsListView(StaffRequiredMixin, ListView):
    model = Meal
    template_name = 'programs/nutrition/meals-list.html'
    context_object_name = "meals"

    def get_queryset(self):
        return Meal.objects.all().order_by('name')


# Supplement
class CreateSupplementView(StaffRequiredMixin, CreateView):
    model = Supplement
    form_class = SupplementForm
    template_name = 'programs/nutrition/supplement-create.html'

    def get_success_url(self):
        return reverse_lazy('supplement-list', kwargs={'slug': self.request.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class SupplementListView(StaffRequiredMixin, ListView):
    model = Supplement
    template_name = 'programs/nutrition/supplements-list.html'
    context_object_name = "supplements"

    def get_queryset(self):
        return Supplement.objects.all().order_by('name')


class EditSupplementView(StaffRequiredMixin, UpdateView):
    model = Supplement
    form_class = SupplementForm
    template_name = 'programs/nutrition/supplement-edit.html'
    context_object_name = 'supplement'

    def get_success_url(self):
        return reverse_lazy('supplement-list', kwargs={'slug': self.request.user.profile.slug})


class DeleteSupplementView(StaffRequiredMixin, DeleteView):
    model = Supplement
    context_object_name = 'supplement'

    def get_success_url(self):
        return reverse_lazy('supplement-list', kwargs={'slug': self.request.user.profile.slug})


class CreateSupplementInstanceView(StaffRequiredMixin, CreateView):
    model = SupplementInstance
    form_class = SupplementInstanceForm
    template_name = 'programs/nutrition/supplement-instance-create.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the NutritionPlan object based on the primary key from the URL
        self.nutrition_plan = get_object_or_404(NutritionPlan, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Associate the supplement instance with the fetched nutrition plan
        form.instance.nutrition_plan = self.nutrition_plan
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nutrition_plan'] = self.nutrition_plan
        return context

    def get_success_url(self):
        profile = self.object.nutrition_plan.user.profile
        return reverse_lazy('nutrition-plan-details', kwargs={
            'slug': profile.slug,
            'pk': self.nutrition_plan.pk
        })


class EditSupplementInstanceView(StaffRequiredMixin, UpdateView):
    model = SupplementInstance
    form_class = SupplementInstanceForm
    template_name = 'programs/nutrition/supplement-instance-edit.html'
    context_object_name = 'supplement'

    def get_success_url(self):
        nutrition_plan = self.object.nutrition_plan
        return reverse_lazy('nutrition-plan-details',
                            kwargs={'pk': nutrition_plan.id, 'slug': nutrition_plan.user.profile.slug})


class DeleteSupplementInstanceView(StaffRequiredMixin, DeleteView):
    model = SupplementInstance

    def get_success_url(self):
        nutrition_plan = self.object.nutrition_plan
        return reverse_lazy('nutrition-plan-details',
                            kwargs={'pk': nutrition_plan.id, 'slug': nutrition_plan.user.profile.slug})


# RecoveryPlan
class RecoveryPlansListView(LoginRequiredMixin, ListView):
    model = RecoveryPlan
    template_name = 'programs/recovery/recovery-plans-list.html'
    context_object_name = 'recovery_plans'

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
        return RecoveryPlan.objects.filter(user=self.profile.user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile  # user being viewed
        context['current_user'] = self.request.user  # logged-in user
        context['recovery_plans'] = RecoveryPlan.objects.filter(user_id=self.profile.user_id)
        return context


class RecoveryDetailView(LoginRequiredMixin, DetailView):
    model = RecoveryPlan
    template_name = 'programs/recovery/recovery-details.html'
    context_object_name = 'recovery_plan'

    def get_queryset(self):
        # Optionally restrict staff access to users they manage
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recovery_plan = self.object
        context['profile'] = recovery_plan.user.profile

        return context


class RecoveryCreateView(StaffRequiredMixin, CreateView):
    model = RecoveryPlan
    form_class = RecoveryPlanForm
    template_name = 'programs/recovery/recovery-create.html'
    context_object_name = 'recovery_plan'

    def get_success_url(self):
        recovery_plan = self.object
        return reverse_lazy('recovery-plan_details', kwargs={'pk': recovery_plan.id, 'slug':recovery_plan.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class RecoveryEditView(StaffRequiredMixin, UpdateView):
    model = RecoveryPlan
    context_object_name = 'recovery_plan'
    form_class = RecoveryPlanForm
    template_name = 'programs/recovery/recovery-edit.html'

    def get_success_url(self):
        recovery_plan = self.object
        return reverse_lazy('recovery-plan_details', kwargs={'pk': recovery_plan.id, 'slug':recovery_plan.user.profile.slug})

    def form_valid(self, form):
        return super().form_valid(form)


class RecoveryDeleteView(StaffRequiredMixin, DeleteView):
    model = RecoveryPlan

    def get_success_url(self):
        profile = self.object.user.profile
        return reverse_lazy('account-detail', kwargs={'slug': profile.slug})


class RecoveryPlanAdminListView(StaffRequiredMixin, ListView):
    model = RecoveryPlan
    template_name = 'programs/recovery/recovery-list-admin.html'
    context_object_name = 'recovery_plans'

    def get_queryset(self):
        return RecoveryPlan.objects.all().order_by('id')