from django.db import models
from django.conf import settings

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    designer = models.CharField(max_length=100)
    year_released = models.IntegerField()
    num_players = models.CharField(max_length=20, default="N/A")
    est_playtime = models.CharField(max_length=50)
    age_recommendation = models.CharField(max_length=20)
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="games")
    categories = models.ManyToManyField("Category", related_name="games")

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Average rating calculated from related Rating objects"""
        ratings = self.ratings.all()
        if ratings.exists():
            total = sum(r.rating for r in ratings)
            return round(total / ratings.count(), 1)
        return None
