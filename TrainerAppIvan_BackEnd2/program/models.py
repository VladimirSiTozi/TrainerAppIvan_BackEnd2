from django.db import models

from TrainerAppIvan_BackEnd2.account.models import AppUser
from TrainerAppIvan_BackEnd2.program.choices import MealTimeChoices


class Trainer(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='trainer_profile')
    # Add additional trainer-specific fields if needed

    def __str__(self):
        return f'{self.user.profile.first_name} {self.user.profile.last_name}'


class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='workout_plans')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='assigned_plans')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} of {self.user}'


class Period(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='periods')
    number = models.PositiveIntegerField()  # 1, 2, 3, or 4
    duration_weeks = models.PositiveIntegerField()  # Duration in weeks

    def __str__(self):
        return f"Period {self.number} of {self.workout_plan.name} of {self.workout_plan.user}"


class Day(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='days')
    number = models.PositiveIntegerField()  # 1, 2, 3, ..., 7
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional: e.g., "Leg Day"

    def __str__(self):
        return f"Day {self.number} of Period {self.period.number} of {self.period.workout_plan.name} of {self.period.workout_plan.user}"


class ExerciseTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    focus = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Chest"

    def __str__(self):
        return self.name


class ExerciseInstance(models.Model):
    exercise_template = models.ForeignKey(ExerciseTemplate, on_delete=models.CASCADE, related_name='instances')
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='exercises')
    sets = models.PositiveIntegerField()
    reps = models.CharField(max_length=50)
    rest = models.CharField(max_length=50)  # e.g., "60s", "2min"
    progression = models.CharField(max_length=100, blank=True, null=True)
    aim = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)  # e.g., "70kg", "Bodyweight"
    tempo = models.CharField(max_length=50, blank=True, null=True)  # e.g., "2-0-2"

    def __str__(self):
        return f"{self.exercise_template.name} on {self.day}"


# NutritionPlan
class NutritionPlan(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # Use JSONField for multiple notes
    trainer_notes = models.JSONField(blank=True, null=True, default=list)
    meal_timing_notes = models.JSONField(blank=True, null=True, default=list)

    target_calories = models.CharField(max_length=50)
    protein_grams = models.CharField(max_length=50)
    carbs_grams = models.CharField(max_length=50)
    fats_grams = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} of {self.user.profile.get_full_name() or self.user.email}"


class Meal(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Grilled Chicken Bowl"

    calories = models.PositiveIntegerField()
    protein_grams = models.FloatField()
    carbs_grams = models.FloatField()
    fats_grams = models.FloatField()

    foods_description = models.TextField(help_text="List of foods and portions included in the meal")

    def __str__(self):
        return f"{self.name}"


class MealInstance(models.Model):
    nutrition_plan = models.ForeignKey(NutritionPlan, related_name='meal_instances', on_delete=models.CASCADE)
    meal_template = models.ForeignKey(Meal, on_delete=models.CASCADE)

    time_of_day = models.CharField(
        max_length=50,
        blank=True,
        choices=MealTimeChoices.choices,
    )

    def __str__(self):
        return f"{self.time_of_day} – {self.meal_template.name}"


class Supplement(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SupplementInstance(models.Model):
    nutrition_plan = models.ForeignKey(NutritionPlan, related_name='supplements', on_delete=models.CASCADE)
    supplement_template = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100, blank=True)
    protein_grams = models.FloatField(blank=True, null=True, help_text="Protein content per serving (optional)")


class RecoveryPlan(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    active_recovery = models.TextField(blank=True, null=True)
    sleep_and_rest = models.TextField(blank=True, null=True)
    self_care = models.TextField(blank=True, null=True)
    monitoring_follow_up = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} of {self.user.trainer_profile.get_full_name() or self.user.email}"
