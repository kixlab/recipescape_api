import json
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipe_api.models import Clustering
from recipe_api.serializers import ClusteringSerializer, RecipeSerializer
from tagger_api.models import Recipe, Annotation


@api_view(['GET'])
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, origin_id=recipe_id)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_recipes(request, dish):
    recipes = get_list_or_404(Recipe, group_name=dish)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clusters(request, dish):
    """
    Return all clusters for given dish
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
    tags = annotation.annotations
    instructions = recipe.instructions['instructions']
    nodes = []
    current_node = {"word": "", "ingredient": []}
    for tag in tags:
        if current_node["word"] == "" and tag['tag'] == 0:
            current_node["word"] = get_word(instructions, tag['index'])
        elif current_node["word"] != "" and tag['tag']== 0:
            nodes.append(current_node)
            current_node = {"word": "", "ingredient": []}
        elif current_node["word"] == "" and tag['tag'] == 0:
            pass
        elif current_node["word"] != "" and tag['tag'] == 1:
            current_node['ingredient'].append(get_word(instructions, tag['index']))
    return nodes


def get_word(instructions, index):
    """
    :param instruction: json object of instruction.
    :param index: [int, int, int]
    :return:
    """
    sentences  = instructions[index[0]]
    tokens = sentences[index[1]]
    word = tokens['tokens'][index[2]]['originalText']
    return word.lower()


