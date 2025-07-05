import json
import re

from django import forms

from .choices import MealTimeChoices
from .models import WorkoutPlan, Period, Day, ExerciseInstance, ExerciseTemplate, NutritionPlan, Meal, Supplement, \
    MealInstance, SupplementInstance, RecoveryPlan
from ..account.models import AppUser


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'user']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Workout Plan Title (e.g., 4-Week Strength Program)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief overview of the workout plan (e.g., Full-body strength training, 3 days/week)...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = AppUser.objects.all().order_by('email')


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['number', 'duration_weeks']
        widgets = {
            'number': forms.NumberInput(attrs={'min': 1, 'max': 4}),
            'duration_weeks': forms.NumberInput(attrs={'min': 1}),
        }


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['number', 'name']
        widgets = {
            'number': forms.NumberInput(attrs={'min': 1, 'max': 7}),
        }


class ExerciseInstanceForm(forms.ModelForm):
    class Meta:
        model = ExerciseInstance
        fields = ['exercise_template', 'order', 'sets', 'reps', 'rest', 'progression', 'aim', 'weight', 'tempo']
        widgets = {
            'exercise_template': forms.Select(attrs={
                'class': 'form-control',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'order of the exercise',
            }),
            'sets': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 3',
            }),
            'reps': forms.TextInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'e.g. 8-12',
            }),
            'rest': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 60s',
            }),
            'progression': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Increase weight each week',
            }),
            'aim': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Hypertrophy',
            }),
            'weight': forms.TextInput(attrs={
                'class': 'form-control',
                'step': 0.1,
                'placeholder': 'e.g. 40.5',
            }),
            'tempo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2-1-2',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise_template'].queryset = ExerciseTemplate.objects.all().order_by('name')
        self.empty_permitted = True


class ExerciseTemplateForm(forms.ModelForm):
    class Meta:
        model = ExerciseTemplate
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter exercise template name (e.g., Bench Press, Squat, Pull-Ups)',
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the workout exercise '
                               '(e.g., Targets chest and triceps; performed on a flat bench with controlled motion)...',
            }),
            'focus': forms.TextInput(attrs={
                'placeholder': 'e.g., Chest, Legs, Full Body, Core',
            }),
        }
        labels = {
            'name': 'Exercise Name',
            'description': 'Description',
            'focus': 'Target Muscle Group/s',
        }

    def clean_youtube_url(self):
        url = self.cleaned_data['youtube_url']
        if not url:
            return ''

        # Extract video ID from various formats
        regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(regex, url)
        if match:
            self.cleaned_data['youtube_video_id'] = match.group(1)
            return url
        raise forms.ValidationError("Invalid YouTube URL")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.youtube_video_id = self.cleaned_data.get('youtube_video_id', '')
        if commit:
            instance.save()
        return instance


# Nutrition
class NutritionPlanForm(forms.ModelForm):
    trainer_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'E.g., Include more protein-rich foods\nLimit processed sugars\nStay hydrated\n...'
        }),
        required=False,
        help_text='Add every item in a new line',
    )
    meal_timing_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'E.g., Breakfast at 7:30 AM\nSnack at 10:00 AM\nLunch at 1:00 PM\nDinner before 8:00 PM'
        }),
        required=False,
        help_text='Add every item in a new line',
    )

    class Meta:
        model = NutritionPlan
        fields = [
            'name',
            'user',
            'description',
            'trainer_notes',
            'meal_timing_notes',
            'target_calories',
            'protein_grams',
            'carbs_grams',
            'fats_grams',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nutrition Plan Title',
            }),
            'user': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select User',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the nutrition plan...',
            }),
            'target_calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2000',
            }),
            'protein_grams': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 150',
            }),
            'carbs_grams': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 250',
            }),
            'fats_grams': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 70',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = AppUser.objects.all().order_by('email')


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = [
            'name',
            'calories',
            'protein_grams',
            'carbs_grams',
            'fats_grams',
            'foods_description',
        ]
        labels = {
            'name': 'Meal Name',
            'calories': 'Total Calories',
            'protein_grams': 'Protein (grams)',
            'carbs_grams': 'Carbohydrates (grams)',
            'fats_grams': 'Fats (grams)',
            'foods_description': 'Description of Foods...',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'E.g., Breakfast, Post-workout Snack',
                'class': 'form-control',
            }),
            'calories': forms.NumberInput(attrs={
                'placeholder': 'E.g., 450',
                'class': 'form-control',
            }),
            'protein_grams': forms.NumberInput(attrs={
                'placeholder': 'E.g., 30',
                'class': 'form-control',
            }),
            'carbs_grams': forms.NumberInput(attrs={
                'placeholder': 'E.g., 50',
                'class': 'form-control',
            }),
            'fats_grams': forms.NumberInput(attrs={
                'placeholder': 'E.g., 15',
                'class': 'form-control',
            }),
            'foods_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'List all foods included in this meal with quantities '
                               '(e.g., 2 eggs, 1 slice whole wheat toast, 1 cup spinach)...',
                'class': 'form-control',
            }),
        }


class MealInstanceForm(forms.ModelForm):
    class Meta:
        model = MealInstance
        exclude = ['nutrition_plan']
        widgets = {
            'time_of_day': forms.Select(choices=MealTimeChoices.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meal_template'].queryset = Meal.objects.all().order_by('name')


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = '__all__'

        labels = {
            'name': 'Supplement Name',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Supplement Name...',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Supplement.objects.order_by('name')


class SupplementInstanceForm(forms.ModelForm):
    class Meta:
        model = SupplementInstance
        exclude = ['nutrition_plan']

        widgets = {
            'dosage': forms.TextInput(attrs={
                'placeholder': 'e.g., 3 times daily',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplement_template'].queryset = Supplement.objects.all().order_by('name')


class RecoveryPlanForm(forms.ModelForm):
    class Meta:
        model = RecoveryPlan
        fields = '__all__'

        help_texts = {
            'name': 'Enter a title for the recovery plan (e.g. "Post-Marathon Recovery").',
            'description': 'Optional. Add an overview of the recovery strategy...',
            'active_recovery': 'Add every new item in a new line',
            'sleep_and_rest': 'Add every new item in a new line',
            'self_care': 'Add every new item in a new line',
            'monitoring_follow_up': 'Add every new item in a new line',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recovery Plan Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the plan...',
                'rows': 3,
            }),
            'active_recovery': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., Light yoga on rest days\nWalking for 30 minutes\n'
                               'Foam rolling after workouts\nStretching before bed',
                'rows': 4,
            }),
            'sleep_and_rest': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Sleep hygiene\nnaps\nrest periods\n...',
                'rows': 4,
            }),
            'self_care': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Massage\nfoam rolling\nsauna\netc.',
                'rows': 4,
            }),
            'monitoring_follow_up': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Check-ins\nadjustments\nmetrics\n...',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = AppUser.objects.all().order_by('email')
