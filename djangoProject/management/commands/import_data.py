from django.core.management.base import BaseCommand
from djangoProject.models import Drug, DrugType, Applicant, Manufacturer, ShelfLife, DrugManufacturer
import csv


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def handle(self, *args, **options):
        self.stdout.write('Starting import...')

        # Імпорт основних даних
        with open('reestr_main_normalized.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Створення або отримання пов'язаних об'єктів
                    drug_type, _ = DrugType.objects.get_or_create(
                        type_name=row['Drug_Type']
                    )

                    applicant, _ = Applicant.objects.get_or_create(
                        name=row['Applicant_Name'],
                        country=row['Applicant_Country'],
                        address=row.get('Applicant_Address', '')
                    )

                    # Створення препарату
                    drug = Drug.objects.create(
                        original_id=row['ID'],  # зберігаємо оригінальний ID
                        trade_name=row['Trade_Name'],
                        international_name=row['International_Name'],
                        form=row['Form'],
                        conditions=row['Conditions'],
                        composition=row['Composition'],
                        pharmacotherapeutic_group=row['Pharmacotherapeutic_Group'],
                        atc_code=row['ATC_Code'],
                        applicant=applicant,
                        registration_number=row['Registration_Number'],
                        drug_type=drug_type
                    )

                    # Створення виробника та зв'язку з препаратом
                    manufacturer, _ = Manufacturer.objects.get_or_create(
                        name=row['Manufacturer_Name'],
                        country=row['Manufacturer_Country'],
                        address=row.get('Manufacturer_Address', '')
                    )

                    # Створення зв'язку через проміжну модель
                    DrugManufacturer.objects.create(
                        drug=drug,
                        manufacturer=manufacturer
                    )

                    # self.stdout.write(f'Successfully imported drug: {drug.trade_name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing drug: {str(e)}'))

        # Імпорт додаткових даних
        with open('reestr_additional_normalized.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    drug = Drug.objects.get(original_id=row.get('ID'))  # змінити на правильну назву колонки
                    ShelfLife.objects.create(
                        drug=drug,
                        bio_origin=row.get('Bio_Origin', '').lower() == 'true',
                        manual_url=row.get('Manual_URL', ''),
                        shelf_life=row.get('Shelf_Life', ''),
                        shelf_life_value=float(row.get('Shelf_Life_Value', 0)) if row.get('Shelf_Life_Value') else None,
                        shelf_life_unit=row.get('Shelf_Life_Unit', '')
                    )
                except Drug.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Drug not found for ID: {row.get("ID")}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing shelf life: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Data import completed'))
