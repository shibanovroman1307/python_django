from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):
    help = 'Normalize data from CSV file'

    def handle(self, *args, **options):
        self.stdout.write('Starting data normalization...')

        try:
            # Зчитування CSV файлу
            filename = 'reestr_main.csv'

            # Визначення назв колонок англійською
            columns_english = [
                'ID', 'Trade_Name', 'International_Name', 'Form', 'Conditions',
                'Composition', 'Pharmacotherapeutic_Group', 'ATC_Code',
                'Applicant_Name', 'Applicant_Country', 'Manufacturer_Name',
                'Manufacturer_Country', 'Registration_Number', 'Start_Date',
                'End_Date', 'Drug_Type'
            ]

            # Зчитування даних з правильним кодуванням
            df = pd.read_csv(filename, encoding='utf-8')

            # Призначення нових назв колонкам
            df.columns = columns_english

            # Нормалізація дат
            date_columns = ['Start_Date', 'End_Date']
            for column in date_columns:
                df[column] = pd.to_datetime(df[column], format='%d.%m.%y', errors='coerce')

            # Очищення текстових даних
            text_columns = df.select_dtypes(include=['object']).columns
            for column in text_columns:
                df[column] = df[column].str.strip()

            # Заповнення пропущених значень
            df = df.fillna('')

            # Збереження нормалізованих даних
            df.to_csv('reestr_main_normalized.csv', index=False, encoding='utf-8')

            self.stdout.write(self.style.SUCCESS('Data normalization completed successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during normalization: {str(e)}'))