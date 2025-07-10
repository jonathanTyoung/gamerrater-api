from django.db import models
from django.conf import settings

class Review(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')  # Enforce one review per user per game
    
    def __str__(self):
        return f"Review by {self.user} on {self.game}"