from django.core.management.base import BaseCommand, CommandError
from mturk_scraper.models import RecipeURL


class Command(BaseCommand):
    help = 'Import recipe urls from text file'

    def add_arguments(self, parser):
        parser.add_argument('--path', help='Folder where json files are')
        parser.add_argument('--name', help="Which food are these urls for")

    def handle(self, *args, **options):

        text_path = options['path']
        recipe_name = options['name']
        with open(text_path, 'r') as f:
            urls = f.readlines()
            RecipeURL.objects.bulk_create([
                RecipeURL(url=url, group_name=recipe_name)
                for url in urls])
