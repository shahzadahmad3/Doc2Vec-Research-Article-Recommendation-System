from django.core.management.base import BaseCommand
from ...import_csv import import_csv_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path='path/to/Paper data.csv'
        import_csv_data(file_path)
        