from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):
    help = 'Process additional CSV data'

    def handle(self, *args, **options):
        self.stdout.write('Starting CSV data processing...')

        try:
            # Зчитування CSV файлу
            filename = 'reestr_additional.csv'  # шлях до файлу

            # Визначення назв колонок англійською
            columns_english = [
                'ID',
                'Bio_Origin',
                'Plant_Origin',
                'Orphan_Drug',
                'Homeopathic',
                'Early_Termination',
                'Manual_URL',
                'Shelf_Life',
                'Shelf_Life_Value',
                'Shelf_Life_Unit'
            ]

            # Зчитування даних з правильним кодуванням
            df = pd.read_csv(filename, encoding='utf-8')

            # Призначення нових назв колонкам
            df.columns = columns_english

            # Конвертація значень "Так/Ні" у булеві
            boolean_columns = ['Bio_Origin', 'Plant_Origin', 'Orphan_Drug',
                               'Homeopathic', 'Early_Termination']
            for column in boolean_columns:
                df[column] = df[column].map({'Так': True, 'Ні': False})

            # Очищення текстових даних
            text_columns = ['Manual_URL', 'Shelf_Life']
            for column in text_columns:
                df[column] = df[column].str.strip()

            # Конвертація числових значень
            df['Shelf_Life_Value'] = pd.to_numeric(df['Shelf_Life_Value'], errors='coerce')

            # Збереження нормалізованих даних
            df.to_csv('reestr_additional_normalized.csv', index=False, encoding='utf-8')

            self.stdout.write(self.style.SUCCESS('CSV data processed successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing CSV: {str(e)}'))