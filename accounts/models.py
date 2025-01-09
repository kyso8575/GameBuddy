from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, blank=False, null=False, verbose_name="닉네임")
    age = models.IntegerField(max_length=10, blank=False, null=False)
    gender = models.CharField(max_length=15)
    preference1 = models.CharField(max_length=30)
    preference2 = models.CharField(max_length=30)

    def __str__(self):
        return self.username