import django.contrib.postgres.fields as pgfields
from django.db import models


class Recipe(models.Model):
    origin_id = models.CharField(max_length=255, unique=True)
    group_name = models.CharField(max_length=100, default="Etc")
    title = models.TextField()
    image_url = models.URLField()
    ingredients = pgfields.ArrayField(models.TextField())
    instructions = pgfields.JSONField()

    def __str__(self):
        return self.title

    """
    An element of instructions field is a step.
    Each step looks like
    {
        "sentences": [
            { "tokens": [ { "text": "Preheat", after: " ", "pos": "NN" }, { "text": "oven", "after": " ", "pos": "TO" }, ...]},
            { "tokens": [ { "text": "Reduce", "after: " ", "pos": "NN" }, ...
        ]
    }
    """


class Annotation(models.Model):
    recipe_id = models.ForeignKey(Recipe)
    annotator = models.CharField(max_length=100, blank=False)
    annotated_at = models.DateField(auto_now_add=True)
    annotations = pgfields.JSONField()

    def __str__(self):
        return self.recipe_id.title + "_" + self.annotated_at.__str__()
