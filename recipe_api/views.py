from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tagger_api.models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET'])
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, origin_id=recipe_id)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_dish(request, dish):
    print(dish)
    recipes = get_list_or_404(Recipe, group_name=dish)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)
