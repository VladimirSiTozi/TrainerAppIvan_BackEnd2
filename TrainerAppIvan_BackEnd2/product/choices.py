from django.utils.translation import gettext_lazy as _


class ProductTypeChoices:
    TRAINING_PLAN = 'training program'
    NUTRITION_PLAN = 'nutrition plan'
    RECOVERY = 'recovery plan'

    CHOICES = [
        (TRAINING_PLAN, _('Training Program')),
        (NUTRITION_PLAN, _('Nutrition Plan')),
        (RECOVERY, _('Recovery Plan')),
    ]


class ProductCategoryChoices:
    GYM = 'gym'
    MARTIAL_ARTS = 'martial_arts'

    CHOICES = [
        (GYM, _('Gym')),
        (MARTIAL_ARTS, _('Martial Arts')),
    ]
