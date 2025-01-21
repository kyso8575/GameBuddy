from django.db import models
from django.contrib.auth.models import User  # Django의 기본 User 모델을 사용

# Create your models here.

class ChatSession(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # 외래 키로 연결
    messages = models.JSONField()  # 사용자 메시지를 JSON 형식으로 저장
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시각

    def __str__(self):
        return f"Session {self.id} for User at {self.created_at}"
        # return f"Session {self.id} for User {self.user.username} at {self.created_at}"