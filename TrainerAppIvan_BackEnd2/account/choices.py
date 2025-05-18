from django.db import models


class SocialMediaChoices(models.TextChoices):
    WHATSAPP = 'whatsapp', 'WhatsApp'
    VIBER = 'viber', 'Viber'
    FACEBOOK = 'facebook', 'Facebook'
    INSTAGRAM = 'instagram', 'Instagram'
    TWITTER = 'twitter', 'Twitter (X)'
    OTHER = 'other', 'Other'
