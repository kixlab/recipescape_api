import json
from tagger_api.models import Recipe
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

def process_recipe(file_path, group_name):
    with open(file_path) as f:
        data = json.load(f)
    print(file_path)

    instructions = []
    for step in data['instructions']:
        parsed_resp = nlp.annotate(step, properties={
            'annotators': 'pos',
            'outputFormat': 'json'
        })
        if type(parsed_resp) is str:
            parsed_resp = json.loads(parsed_resp.replace('\u0000', ''), encoding='utf-8', strict=False)
        instructions.append(parsed_resp["sentences"])

    new_recipe = Recipe.objects.create(title=data['name'],
                                       image_url=data['image_addr'],
                                       origin_id=data['id'],
                                       ingredients=data['ingredients'],
                                       instructions={"instructions": instructions},
                                       group_name=group_name)
    new_recipe.save()
