import json
from tagger_api.models import Recipe
import requests
from urllib.parse import quote

parser_host = 'http://localhost:9000/'
parser_option = "{'annotators': 'tokenize,ssplit,pos', 'outputFormat': 'json'}"
parser_option_encoded = quote(parser_option)
parser_url = parser_host + "?properties=" + parser_option_encoded

def process_recipe(file_path, group_name):
    with open(file_path) as f:
        data = json.load(f)

    instructions = []
    for step in data['instructions']:

        resp = requests.post(parser_url, data=step.encode('utf-8'))
        resp.encoding = 'utf-8'
        parsed_resp = json.loads(resp.text.replace('\u0000', ''), strict=False)
        instructions.append(parsed_resp["sentences"])

    new_recipe = Recipe.objects.create(title=data['name'],
                                       image_url=data['image_addr'],
                                       origin_id=data['id'],
                                       ingredients=data['ingredients'],
                                       instructions={"instructions": instructions},
                                       group_name=group_name)
    new_recipe.save()
