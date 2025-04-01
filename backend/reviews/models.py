from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """Game review model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    game = models.ForeignKey(
        'games.Game',  # Reference to 'Game' model in 'games' app
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Constraint to prevent a user from writing multiple reviews for the same game
        unique_together = ['user', 'game']

    def __str__(self):
        return f"{self.user.username}'s review for {self.game.name} ({self.rating}/5)"
