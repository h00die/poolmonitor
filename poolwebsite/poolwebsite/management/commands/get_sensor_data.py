from django.core.management.base import BaseCommand, CommandError
from poolmonitor import tasks

class Command(BaseCommand):
    args = ''
    help = 'Pulls data from the sensors'

    def handle(self, *args, **options):
        tasks.read_sensors()