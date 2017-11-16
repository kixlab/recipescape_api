from django.core.management.base import BaseCommand, CommandError
from ._dummy_cluster import run_cluster
from ._load_cluster import load_cluster

class Command(BaseCommand):
    help = 'Import recipes from json, add machine POS, and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--title', help="The title of current clustering job")
        parser.add_argument('--dishname', help="Which group of recipe will you cluster")
        parser.add_argument('--points', help="The path of cluster result")
        parser.add_argument('--centers', help="The path of cluster center")

    def handle(self, *args, **options):
        if options['points']:
            load_cluster(options['title'], options['dishname'], options['points'], options['centers'])
        else: # dummy
            run_cluster(options['title'], options['dishname'])
