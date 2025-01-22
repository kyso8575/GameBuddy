from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """커스텀 사용자 모델"""

    # 📸 프로필 이미지 필드
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/default_profile.png'
    )

    def __str__(self):
        return self.username
