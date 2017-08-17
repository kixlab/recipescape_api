import json
import datetime

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from tagger_api.models import Recipe, Annotation
from tagger_api.serializers import RecipeSerializer, AnnotationSerializer


@api_view(['GET'])
def new_recipe(request):
    """
    Return a recipe without annotation
    :param request:
    :return: Recipe
    """
    dt_10mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
    fresh_recipe = Recipe.objects.filter(annotation__isnull=True) \
                                 .filter(last_assigned__lte=dt_10mins_ago) \
                                 .order_by('group_name') \
                                 .first()
    fresh_recipe.last_assigned = timezone.now()
    print(fresh_recipe.last_assigned)
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
