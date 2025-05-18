import datetime

from django.contrib.auth import get_user_model
from django.db import models

from TrainerAppIvan_BackEnd2.account.choices import SocialMediaChoices

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    phone_number = models.CharField(
        blank=True,
        null=True,
    )

    preferred_social_media = models.CharField(
        max_length=30,
        choices=SocialMediaChoices.choices,
        blank=True,
        null=True,
    )

    social_media_url = models.URLField(
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )

    is_profile_complete = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Profile object ({self.user})"

    def age(self):
        if self.date_of_birth:
            today = datetime.date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
