from django.db import models


class MealTimeChoices(models.TextChoices):
    BREAKFAST = 'Breakfast', 'Breakfast'
    MORNING_SNACK = 'Morning Snack', 'Morning Snack'
    LUNCH = 'Lunch', 'Lunch'
    AFTERNOON_SNACK = 'Afternoon Snack', 'Afternoon Snack'
    DINNER = 'Dinner', 'Dinner'
    EVENING_SNACK = 'Evening Snack', 'Evening Snack'
