from django.db import models
import json

# Create your models here.


class Game(models.Model):
    id = models.IntegerField(primary_key=True)  # ID field that doesn't auto-increment
    name = models.CharField(max_length=255)
    released = models.DateField(null=True, blank=True)  # released date allows NULL
    background_image = models.URLField(null=True, blank=True)  # background_image allows NULL
    rating = models.FloatField(default=0, null=True, blank=True)  # rating allows NULL
    metacritic_score = models.IntegerField(default=0, null=True, blank=True)  # metacritic_score allows NULL
    playtime = models.IntegerField(default=0, null=True, blank=True)  # playtime allows NULL
    platforms = models.TextField(null=True, blank=True)  # platforms stored as string
    genres = models.TextField(null=True, blank=True)  # genres stored as string
    stores = models.CharField(max_length=255, null=True, blank=True)  # stores allows NULL
    esrb_rating = models.CharField(max_length=255, null=True, blank=True)  # esrb_rating allows NULL
    description = models.TextField(null=True, blank=True)  # description allows NULL
    screenshots = models.TextField(null=True, blank=True)  # screenshots stored as string

    def __str__(self):
        return self.name

    def get_platforms(self):
        # Parse JSON string into a list
        return json.loads(self.platforms) if self.platforms else []

    def set_platforms(self, platforms):
        # Convert list to JSON string for storage
        self.platforms = json.dumps(platforms)

    def get_genres(self):
        # Parse JSON string into a list
        return json.loads(self.genres) if self.genres else []

    def set_genres(self, genres):
        # Convert list to JSON string for storage
        self.genres = json.dumps(genres)

    def get_screenshots(self):
        # Parse JSON string into a list
        return json.loads(self.screenshots) if self.screenshots else []

    def set_screenshots(self, screenshots):
        # Convert list to JSON string for storage
        self.screenshots = json.dumps(screenshots)
