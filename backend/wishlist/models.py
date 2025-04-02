from django.db import models
from django.contrib.auth import get_user_model
from games.models import Game

User = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'game')  # 사용자당 게임은 한 번만 등록 가능
        ordering = ['-created_at']  # 최신 항목이 먼저 표시
        verbose_name = '위시리스트'
        verbose_name_plural = '위시리스트'
    
    def __str__(self):
        return f"{self.user.username}의 위시리스트: {self.game.name}"
