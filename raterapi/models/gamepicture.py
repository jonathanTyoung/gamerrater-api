from django.db import models
from raterapi.models import Game  # Make sure Game is imported correctly

class GamePicture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='pictures')
    action_pic = models.ImageField(
        upload_to='actionimages/',
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Picture for {self.game.title}"
