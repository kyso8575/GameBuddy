from django.db import models
import json

# Create your models here.

# class Game(models.Model):
#     name = models.CharField(max_length=255)
#     released = models.DateField(null=True, blank=True)  # released는 NULL 허용
#     background_image = models.URLField(null=True, blank=True)  # background_image는 NULL 허용
#     rating = models.FloatField(default=0, null=True, blank=True)  # rating은 NULL 허용
#     metacritic_score = models.IntegerField(default=0, null=True, blank=True)  # metacritic_score는 NULL 허용
#     playtime = models.IntegerField(default=0, null=True, blank=True)  # playtime은 NULL 허용
#     platforms = models.JSONField(null=True, blank=True)  # platforms는 NULL 허용
#     genres = models.JSONField(null=True, blank=True)  # genres는 NULL 허용
#     stores = models.CharField(max_length=255, null=True, blank=True)  # stores는 NULL 허용
#     esrb_rating = models.CharField(max_length=255, null=True, blank=True)  # esrb_rating은 NULL 허용
#     screenshots = models.JSONField(null=True, blank=True)  # screenshots는 NULL 허용

#     def __str__(self):
#         return self.name


class Game(models.Model):
    name = models.CharField(max_length=255)
    released = models.DateField(null=True, blank=True)  # released는 NULL 허용
    background_image = models.URLField(null=True, blank=True)  # background_image는 NULL 허용
    rating = models.FloatField(default=0, null=True, blank=True)  # rating은 NULL 허용
    metacritic_score = models.IntegerField(default=0, null=True, blank=True)  # metacritic_score는 NULL 허용
    playtime = models.IntegerField(default=0, null=True, blank=True)  # playtime은 NULL 허용
    platforms = models.TextField(null=True, blank=True)  # platforms는 문자열로 저장
    genres = models.TextField(null=True, blank=True)  # genres는 문자열로 저장
    stores = models.CharField(max_length=255, null=True, blank=True)  # stores는 NULL 허용
    esrb_rating = models.CharField(max_length=255, null=True, blank=True)  # esrb_rating은 NULL 허용
    screenshots = models.TextField(null=True, blank=True)  # screenshots는 문자열로 저장

    def __str__(self):
        return self.name

    def get_platforms(self):
        # JSON 형식의 문자열을 파싱하여 리스트로 반환
        return json.loads(self.platforms) if self.platforms else []

    def set_platforms(self, platforms):
        # 리스트를 JSON 형식의 문자열로 변환하여 저장
        self.platforms = json.dumps(platforms)

    def get_genres(self):
        # JSON 형식의 문자열을 파싱하여 리스트로 반환
        return json.loads(self.genres) if self.genres else []

    def set_genres(self, genres):
        # 리스트를 JSON 형식의 문자열로 변환하여 저장
        self.genres = json.dumps(genres)

    def get_screenshots(self):
        # JSON 형식의 문자열을 파싱하여 리스트로 반환
        return json.loads(self.screenshots) if self.screenshots else []

    def set_screenshots(self, screenshots):
        # 리스트를 JSON 형식의 문자열로 변환하여 저장
        self.screenshots = json.dumps(screenshots)
