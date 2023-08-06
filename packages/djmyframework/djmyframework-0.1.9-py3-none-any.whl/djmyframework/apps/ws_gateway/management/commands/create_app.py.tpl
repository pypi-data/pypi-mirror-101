
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = (""" help"""
    )
    missing_args_message = "missing_args_message"


    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('args', nargs='*')


    def handle(self, **options):
        print('handle')
