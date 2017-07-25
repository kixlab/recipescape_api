import os
from django.core.management.base import BaseCommand, CommandError
from ._recipe_handler import process_recipe
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Import recipes from json, add machine POS, and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--json_dirs', nargs='+', help='Folder where json files are')
        parser.add_argument('--name', help="Which kind of recipe the folder contains")

    def handle(self, *args, **options):
        print(options)
        for json_dir in options['json_dirs']:
            json_dir = os.path.abspath(json_dir)
            print(json_dir)
            files = [os.path.join(json_dir, filepath) for filepath in os.listdir(json_dir)]
            for file in tqdm(files):
                process_recipe(file, options['name'])