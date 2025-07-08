from django.db import models
from django.conf import settings

class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    designer = models.CharField(max_length=255, blank=True, null=True)
    year_released = models.IntegerField(blank=True, null=True)
    num_players = models.CharField(max_length=100, blank=True, null=True)
    est_playtime = models.CharField(max_length=100, blank=True, null=True)
    age_recommendation = models.CharField(max_length=100, blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # or 'raterapi.Player' if you have a custom Player model
        on_delete=models.CASCADE,
        related_name='games'
    )

    def __str__(self):
        return self.title