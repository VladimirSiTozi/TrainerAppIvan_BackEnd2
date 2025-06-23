import json

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
            'description': forms.Textarea(attrs={'rows': 3}),
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
        fields = ['exercise_template', 'sets', 'reps', 'rest', 'progression', 'aim', 'weight', 'tempo']
        widgets = {
            'sets': forms.NumberInput(attrs={'min': 1}),
            'rest': forms.TextInput(attrs={'placeholder': 'e.g. 60s'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise_template'].queryset = ExerciseTemplate.objects.all().order_by('name')
        self.empty_permitted = True


class ExerciseTemplateForm(forms.ModelForm):
    class Meta:
        model = ExerciseTemplate
        fields = ['name', 'description', 'focus']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'focus': forms.TextInput(attrs={'placeholder': 'e.g., Chest, Legs'}),
        }
        labels = {
            'name': 'Exercise Name',
            'description': 'Description (optional)',
            'focus': 'Target Muscle Group',
        }


# Nutrition
class NutritionPlanForm(forms.ModelForm):
    trainer_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text='Enter a JSON list, e.g., ["note 1", "note 2"]'
    )
    meal_timing_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text='Enter a JSON list, e.g., ["Breakfast", "Lunch"]'
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

    def clean_trainer_notes(self):
        data = self.cleaned_data['trainer_notes']
        print(data)
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if not isinstance(parsed, list):
                    raise forms.ValidationError("Must be a list of trainer notes.")
                return parsed
            except json.JSONDecodeError:
                raise forms.ValidationError("Enter valid JSON.")
        return data

    def clean_meal_timing_notes(self):
        data = self.cleaned_data.get('meal_timing_notes', '')
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, list):
                raise forms.ValidationError("Meal timing notes must be a JSON list.")
            return parsed
        except json.JSONDecodeError:
            raise forms.ValidationError("Enter a valid JSON list for meal timing notes.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Instance trainer_notes:", self.instance.trainer_notes)
        if self.instance and self.instance.pk:
            self.fields['trainer_notes'].initial = json.dumps(self.instance.trainer_notes or [])
            self.fields['meal_timing_notes'].initial = json.dumps(self.instance.meal_timing_notes or [])


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
        widgets = {
            'foods_description': forms.Textarea(attrs={'rows': 3}),
        }


class MealInstanceForm(forms.ModelForm):
    class Meta:
        model = MealInstance
        exclude = ['nutrition_plan']
        widgets = {
            'time_of_day': forms.Select(choices=MealTimeChoices.choices),
        }


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Supplement.objects.order_by('name')


class SupplementInstanceForm(forms.ModelForm):
    class Meta:
        model = SupplementInstance
        exclude = ['nutrition_plan']


from django import forms
from .models import RecoveryPlan

class RecoveryPlanForm(forms.ModelForm):
    class Meta:
        model = RecoveryPlan
        fields = '__all__'

        help_texts = {
            'name': 'Enter a title for the recovery plan (e.g. "Post-Marathon Recovery").',
            'description': 'Optional. Add an overview of the recovery strategy.',
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
                'placeholder': 'Brief description of the plan',
                'rows': 3,
            }),
            'active_recovery': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List active recovery strategies...',
                'rows': 4,
            }),
            'sleep_and_rest': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Sleep hygiene, naps, rest periods...',
                'rows': 4,
            }),
            'self_care': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Massage, foam rolling, sauna, etc.',
                'rows': 4,
            }),
            'monitoring_follow_up': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Check-ins, adjustments, metrics...',
                'rows': 4,
            }),
        }
