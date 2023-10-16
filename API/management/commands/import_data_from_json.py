from django.core.management.base import BaseCommand
from ...utils import import_data_from_file


class Command(BaseCommand):
    help = 'Import photos from JSON file - data.json'

    def handle(self, *args, **kwargs):
        self.stdout.write("Photos are imported into the database ...")

        import_data_from_file()
        self.stdout.write(self.style.SUCCESS('Data has been imported'))
