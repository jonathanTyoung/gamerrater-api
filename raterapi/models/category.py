from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    label = models.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.label