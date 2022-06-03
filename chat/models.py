from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_player = models.BooleanField(default=True)
    is_creator = models.BooleanField(default=False)
    is_validator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
# Create your models here.
