from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Users(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, blank=False, null=False, verbose_name="닉네임")
    age = models.IntegerField(blank=False, null=False)
    gender = models.CharField(max_length=15)
    preference1 = models.CharField(max_length=30)
    preference2 = models.CharField(max_length=30)
    # profile_picture 구현중
        
    groups = models.ManyToManyField(  #충돌이 발생해서 related_name을 만들어 회피함.
        Group,
        related_name="custom_user_groups",  # 기본값인 `user_set` 대신 변경
        blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # 기본값인 `user_set` 대신 변경
        blank=True)

    def __str__(self):
        return self.username