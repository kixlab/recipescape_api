from tagger_api.models import Recipe
from rest_framework import serializers

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('origin_id', 'title', 'image_url', 'ingredients', 'sentences')