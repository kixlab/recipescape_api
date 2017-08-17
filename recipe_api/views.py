import json
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipe_api.models import Clustering
from recipe_api.serializers import ClusteringSerializer, RecipeSerializer
from recipe_api.utils import tree_util
from tagger_api.models import Recipe, Annotation


@api_view(['GET'])
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, origin_id=recipe_id)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_recipes(request, dish):
    """
    Return all recipes for given dish
    :param dish: Kind of recipe (e.g chocolate cookie, potato salad)
    """
    recipes = get_list_or_404(Recipe, group_name=dish)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clusters(request, dish):
    """
    Return all clusters for given dish
    :param dish: Kind of recipe (e.g chocolate cookie, potato salad)
    """
    clusters = get_list_or_404(Clustering, dish_name=dish)
    serializer = ClusteringSerializer(clusters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_tree(request, recipe_id):
    """
    :param request:
    :param recipe_id: origin_id of Recipe model
    :return: [(action, [ingredient])]
    """
    annotation = get_object_or_404(Annotation, recipe=recipe_id)
    recipe = Recipe.objects.get(origin_id=recipe_id)
    nodes = tree_util.make_tree(recipe, annotation)
    return nodes


@api_view(['GET'])
def get_trees(request, dish):
    annotations = Annotation.objects.filter(recipe__group_name=dish).select_related('recipe')
    trees = [{
        'id': annotation.recipe.origin_id,
        'tree': tree_util.make_tree(annotation.recipe, annotation)
    } for annotation in annotations]
    return Response(trees)

@api_view(['GET'])
def get_nodes(request, dish):
    """
    Return list of action and ingredients for each recipe
    """
    annotations = Annotation.objects.filter(recipe__group_name=dish).select_related('recipe')
    nodes = []
    for annotation in annotations:
        tree = tree_util.make_tree(annotation.recipe, annotation)
        actions = set([t['word'] for t in tree])
        ingredients = set([item for t in tree for item in t['ingredient']])
        nodes.append({'id': annotation.recipe.origin_id, 'actions': actions, 'ingredients': ingredients})
    return Response(nodes)

