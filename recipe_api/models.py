from django.db import models
import django.contrib.postgres.fields as pgfields
from tagger_api.models import Recipe

# Create your models here.
class Clustering(models.Model):
    title = models.TextField()
    dish_name = models.TextField()
    points = pgfields.JSONField(default=list([]))
    centers = pgfields.JSONField(default=list([]))
"""
each point looks like
{
    "recipe_id": XXXX,
    "cluster_no": 2,
    "x": 140,
    "y": -110
}

and each cluster looks like
{
    [cluster_no]: <recipe_id>,
}
"""
