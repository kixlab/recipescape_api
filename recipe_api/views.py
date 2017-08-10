from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tagger_api.models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET'])
def get_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(origin_id=recipe_id)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)
