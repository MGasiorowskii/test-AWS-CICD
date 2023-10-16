from django.core.management.base import BaseCommand
from ...utils import import_data_from_api


class Command(BaseCommand):
    help = 'Import photos from external API at https://jsonplaceholder.typicode.com/photos'

    def handle(self, *args, **kwargs):
        self.stdout.write("Photos are imported into the database ...")

        import_data_from_api()
        self.stdout.write(self.style.SUCCESS('Data has been imported'))
