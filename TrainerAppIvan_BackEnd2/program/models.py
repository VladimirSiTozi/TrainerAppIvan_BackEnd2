from django.db import models

from django.db import models

from TrainerAppIvan_BackEnd2.account.models import AppUser


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
