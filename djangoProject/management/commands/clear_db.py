from django.core.management.base import BaseCommand
from djangoProject.models import ShelfLife, DrugManufacturer, Drug, DrugType, Applicant, Manufacturer


class Command(BaseCommand):
    help = 'Clear all data from database tables'

    def handle(self, *args, **options):
        self.stdout.write('Clearing database...')

        # Видалення даних з таблиць у правильному порядку
        ShelfLife.objects.all().delete()
        self.stdout.write('Cleared ShelfLife table')

        DrugManufacturer.objects.all().delete()
        self.stdout.write('Cleared DrugManufacturer table')

        Drug.objects.all().delete()
        self.stdout.write('Cleared Drug table')

        DrugType.objects.all().delete()
        self.stdout.write('Cleared DrugType table')

        Applicant.objects.all().delete()
        self.stdout.write('Cleared Applicant table')

        Manufacturer.objects.all().delete()
        self.stdout.write('Cleared Manufacturer table')

        self.stdout.write(self.style.SUCCESS('Successfully cleared all tables'))