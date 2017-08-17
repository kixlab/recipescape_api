import collections
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
        node = tree_util.make_node(annotation.recipe, annotation)
        nodes.append({'id': annotation.recipe.origin_id, 'actions': node['actions'], 'ingredients': node['ingredients']})
    return Response(nodes)

@api_view(['POST'])
def get_histograms(request, dish):
    """
    For selected clusters,
    count distribution of top 3 actions and ingredients
    """
    cluster_id = request.data['cluster_id']
    selected_cluster = request.data['selected_clusters']
    # cluster = get_object_or_404(Clustering, title=cluster_name)
    cluster = Clustering.objects.get(id=cluster_id)
    selected_ids = [p["recipe_id"] for p in cluster.points if p["cluster_no"] in selected_cluster]

    # I should've normalized table more...ㅜㅜㅜㅜㅜ
    annotations = Annotation.objects.filter(recipe__group_name=dish).select_related('recipe')
    annotations_selected = [annotation for annotation in annotations
                            if annotation.recipe.origin_id in selected_ids]
    nodes = [tree_util.make_node(annotation.recipe, annotation) for annotation in annotations_selected]

    # Get top 3 ingredients and actions
    action_dict = collections.defaultdict(int)
    ingredient_dict = collections.defaultdict(int)
    for node in nodes:
        for action in node['actions']:
            action_dict[action] += 1
        for ingredient in node['ingredients']:
            ingredient_dict[ingredient] += 1
    top3_actions = [kv[0] for kv in sorted(action_dict.items(), key=lambda p: p[1], reverse=True)[:3]]
    top3_ingredients = [kv[0] for kv in sorted(ingredient_dict.items(), key=lambda p: p[1], reverse=True)[:3]]

    # Get distribution of these top 3 actions and ingredients.
    # We normalize bins to size 9, except for the first 3 and the last 3 bins.
    bin_size = 9
    action_bins = collections.defaultdict(lambda: [0 for _ in range(bin_size)])
    ingredient_bins = collections.defaultdict(lambda: [0 for _ in range(bin_size)])
    for node in nodes:
        for action in top3_actions:
            try:
                index = node['actions'].index(action)
            except ValueError:
                continue
            normalized_index = index_normalizer(index, bin_size, len(node['actions']))
            try:
                action_bins[action][normalized_index] += 1
            except IndexError:
                continue
        for ingredient in top3_ingredients:
            try:
                index = node['ingredients'].index(ingredient)
            except ValueError:
                continue
            normalized_index = index_normalizer(index, bin_size, len(node['ingredients']))
            try:
                ingredient_bins[ingredient][normalized_index] += 1
            except IndexError:
                continue

    return Response({
        "top3_actions": action_bins.items(),
        "top3_ingredients": ingredient_bins.items(),
    })



def index_normalizer(index, len_bin, len_node):
    if 0 <= index < 3:
        return index
    elif len_node - 3 <= index < len_node:
        diff = len_node - len_bin
        return index - diff
    else:
        ratio = (len_node - 3) / (len_bin - 3)
        normalized_index = int(index / ratio)
        return normalized_index
