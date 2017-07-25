from django.http import HttpResponse, JsonResponse

from tagger_api.models import Recipe, Annotation


def new_recipe(request):
    fresh_recipe = Recipe.objects.filter(annotation__isnull=True).first()
    return JsonResponse(fresh_recipe)


def get_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return JsonResponse(recipe)


def save_annotation(request, recipe_id):
    annotation = Annotation.objects.create(recipe_id=recipe_id,
                                           annotator=request.POST['annotator'],
                                           annotation=request.POST['annotation'])
    annotation.save()
    return HttpResponse(status=200)
