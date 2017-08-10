import os
from django.core.management.base import BaseCommand, CommandError
from ._dummy_cluster import run_cluster
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Import recipes from json, add machine POS, and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--title', help="The title of current clustering job")
        parser.add_argument('--dishname', help="Which group of recipe will you cluster")

    def handle(self, *args, **options):
        run_cluster(options['title'], options['dishname'])
