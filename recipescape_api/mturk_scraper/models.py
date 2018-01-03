from django.db import models
import random
import string
from .utils import generate_token


class RecipeURL(models.Model):
    url = models.URLField()
    group_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class Assignment(models.Model):
    url = models.ForeignKey(RecipeURL)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=10, default=generate_token)


class ScrapedRecipe(models.Model):
    scraped_by = models.ForeignKey(Assignment)
    title = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    ingredients = models.TextField()
    instruction = models.TextField()
