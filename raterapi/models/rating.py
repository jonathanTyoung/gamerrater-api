from django.db import models
from django.conf import settings
from raterapi.models import Game

class Rating(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(null=False)

    class Meta:
        unique_together = ('game', 'user')

    def __str__(self):
        return f"{self.user} rated {self.game}: {self.rating}"