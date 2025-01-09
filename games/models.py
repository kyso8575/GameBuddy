from django.db import models

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=255)
    released = models.DateField()
    background_image = models.URLField()
    rating = models.FloatField(default=0)
    metacritic_score = models.IntegerField(default=0, null=True)
    playtime = models.IntegerField(default=0)
    platforms = models.JSONField()  # platforms는 여러 개의 플랫폼을 담을 수 있으므로 JSON으로 처리
    genres = models.JSONField()  # genres는 여러 장르를 담을 수 있으므로 JSON으로 처리
    stores= models.CharField(max_length=255)
    esrb_rating = models.CharField(max_length=255)
    screenshots = models.JSONField()  # screenshots도 여러 개 담을 수 있으므로 JSON 처리

    def __str__(self):
        return self.name
