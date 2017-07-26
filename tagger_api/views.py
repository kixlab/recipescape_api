from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from tagger_api.models import Recipe, Annotation


@method_decorator(csrf_exempt, name='dispatch')
def new_recipe(request):
    fresh_recipe = Recipe.objects.filter(annotation__isnull=True).first()
    recipe_json = serializers.serialize('json', [fresh_recipe])

    return HttpResponse(recipe_json, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
def get_recipe(request, recipe_id):
    recipe = Recipe.objects.get(origin_id=recipe_id)
    recipe_json = serializers.serialize('json', [recipe])

    return HttpResponse(recipe_json, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
def save_annotation(request, recipe_id):
    annotation = Annotation.objects.create(recipe_id=recipe_id,
                                           annotator=request.POST['annotator'],
                                           annotation=request.POST['annotation'])
    annotation.save()
    return HttpResponse(status=200)
