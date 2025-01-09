from django.db import models

#검색기능 테스트용
class Animal(models.Model):
        name = models.CharField(max_length=100)
        habitat = models.CharField(max_length=100)
        eating = models.TextField()

        def __str__(self):
            return self.name 