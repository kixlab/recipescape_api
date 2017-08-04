import json

from rest_framework import permissions, status
from rest_framework.decorators import api_view
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
    fresh_recipe = Recipe.objects.filter(annotation__isnull=True).first()
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