import os
import json
from tqdm import tqdm

from django.utils.text import get_valid_filename
from django.core.management.base import BaseCommand, CommandError
from mturk_scraper.models import ScrapedRecipe


class Command(BaseCommand):
    help = 'Import recipe urls from text file'

    def add_arguments(self, parser):
        parser.add_argument('--menu', help='Which menu to export')
        parser.add_argument('--dir', help="Where to put jsons?")


    def handle(self, *args, **options):
        menu = options['menu']
        dir = options['dir']

        scraped_recipes = ScrapedRecipe.objects\
            .filter(scraped_by__url__group_name=menu)
        for scraped in tqdm(scraped_recipes):
            recipe = {
                'id': "{}_{}".format(menu, scraped.id),
                'image_addr': scraped.image_url,
                "ingredients": scraped.ingredients.splitlines(),
                "instructions": scraped.instruction.splitlines(),
                "name": scraped.title,
            }

            file_path = os.path.join(dir,
                                     get_valid_filename(scraped.title + '.json'))
            with open(file_path, 'w') as f:
                json.dump(recipe, f, indent=4)
