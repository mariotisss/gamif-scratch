from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser): # Hereda del usuario base de Django
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.username    # Representación en texto del usuario