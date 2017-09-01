import json
import datetime

from django.db.models import Count
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe_api.utils import tree_util
from tagger_api.models import Recipe, Annotation
from tagger_api.serializers import RecipeSerializer, AnnotationSerializer


@api_view(['GET'])
def new_recipe(request):
    """
    Return a recipe without annotation
    :param request:
    :return: Recipe
    """
    dt_20mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=20)
    fresh_recipe = Recipe.objects.filter(annotation__isnull=True) \
                                 .filter(last_assigned__lte=dt_20mins_ago) \
                                 .order_by('group_name') \
                                 .first()
    fresh_recipe.last_assigned = timezone.now()
    fresh_recipe.save()
    serializer = RecipeSerializer(fresh_recipe, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(origin_id=recipe_id)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_userinfo(request):
    """
    Count the number of recipe processed by given worker
    :param request:
    :return: (Recipe count, Annotation count)
    """
    annotations = Annotation.objects.filter(worker_id=request.user.id)
    recipe_count = annotations.distinct("recipe_id").count()

    return Response({
        "count": {
            "recipe": recipe_count,
        }
    })


class AnnotationView(APIView):
    """
    (GET) List all annotations for a recipe
    (POST) Save annotation for a recipe
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, recipe_id):
        annotations = Annotation.objects.filter(recipe=recipe_id)
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)

    def post(self, request, recipe_id):
        data = json.loads(request.body)
        print(request.user.get_username())
        try:
            recipe = Recipe.objects.get(origin_id=recipe_id)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        annotation = Annotation.objects.create(recipe=recipe,
                                               annotator=data['annotator'],
                                               worker=request.user,
                                               annotations=data['annotation'])
        annotation.save()
        return Response(status=status.HTTP_201_CREATED)


def leaderboard(request):
    users = Annotation.objects.values('annotator')\
                              .annotate(annotation_count=Count('annotator'))\
                              .order_by('-annotation_count')
    annotation_counts = Annotation.objects.count()
    template = loader.get_template('leaderboard.html')
    context = {
        'users': users,
        'count': annotation_counts,
    }
    return HttpResponse(template.render(context, request))


@api_view(['GET'])
def count_corrections(request, dishname):
    annotations = Annotation.objects.filter(recipe__group_name=dishname).select_related('recipe')
    recipe_counts = Recipe.objects.filter(group_name=dishname).count()
    annotation_counts = len(annotations)
    tagged_action_pos_verb = 0
    tagged_action_pos_nonverb = 0
    for annotation in annotations:
        for word in annotation.annotations:
            if word['tag'] is 0:
                location = word['index']
                token = tree_util.get_token(annotation.recipe.instructions['instructions'], location)
                pos = token['pos']
                if pos[0] is 'V':
                    tagged_action_pos_verb += 1
                else:
                    tagged_action_pos_nonverb += 1

    return Response({
        'dishname': dishname,
        'total_recipes': recipe_counts,
        'tagged_recipes': annotation_counts,
        'tagged_action_pos_verb': tagged_action_pos_verb,
        'tagged_action_pos_nonverb': tagged_action_pos_nonverb,
    })
