# Реєстр лікарських засобів

Веб-застосунок для обліку та управління інформацією про лікарські засоби.

## Вимоги
- Python 3.11
- Django 5.1.3
- SQLite/MySQL

## Встановлення та запуск

### 1. Перевірте версію Python:
```bash
python --version
```
### 2. Створіть віртуальне середовище:
```bash
python -m venv .venv
```

### 3. Активуйте віртуальне середовище:
#### Windows:
```bash
.venv\Scripts\activate
```
#### Linux/Mac:
```bash
source .venv/bin/activate
```

### 4. Встановіть залежності:
```bash
pip install -r requirements.txt
```

### 5. Виконайте міграції:
```bash
python manage.py migrate
```

### 6. Створіть суперкористувача:
```bash
python manage.py createsuperuser
```

### 7. Запустіть сервер розробки:
```bash
python manage.py runserver
```

### 8. Виконайте нормалізацію файлу reestr_main.csv:
```bash
python manage.py script_1
```

### 9. Виконайте нормалізацію файлу reestr_additional.csv:
```bash
python manage.py script_2
```

### 10. Виконайте імпорт даних в базу даних:
```bash
python manage.py import_data
```

### 11. Створіть статичні файли:
```bash
python manage.py collectstatic
```

### Після запуску веб-застосунок буде доступний за адресою http://127.0.0.1:8000/

## Функціонал
- Перегляд списку препаратів
- Додавання нових препаратів
- Редагування інформації
- Адміністрування бази даних
