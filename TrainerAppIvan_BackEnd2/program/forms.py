from django import forms
from .models import WorkoutPlan, Period, Day, ExerciseInstance, ExerciseTemplate


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


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
        self.fields['exercise_template'].queryset = ExerciseTemplate.objects.all()
        self.empty_permitted = True