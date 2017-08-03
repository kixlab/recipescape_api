from .models import Recipe, Annotation
from rest_framework import serializers

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('origin_id', 'group_name', 'title', 'image_url', 'ingredients', 'instructions')

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
       model = Annotation
       fields = ('recipe', 'annotator', 'annotations')