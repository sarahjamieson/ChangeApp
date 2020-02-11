from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Band(models.TextChoices):
        BAND_1 = '1'
        BAND_2 = '2'
        BAND_3 = '3'
        BAND_4 = '4'
        BAND_5 = '5'
        BAND_6 = '6'
        BAND_7 = '7'
        BAND_8A = '8a'
        BAND_8B = '8b'
        BAND_8C = '8c'
        BAND_8D = '8d'
        BAND_9 = '9'
        NOT_SET = 'N'
        OTHER = 'O'

    band = models.CharField(
        max_length=2,
        choices=Band.choices,
        default=Band.NOT_SET
    )

    hubs = models.ManyToManyField(
        'db.Hub',
        related_name='staff'
    )

    role = models.CharField(
        max_length=80
    )
