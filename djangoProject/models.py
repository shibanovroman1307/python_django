from django.db import models


# Таблиця типів ліків
class DrugType(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name


# Таблиця заявників
class Applicant(models.Model):
    name = models.TextField()  # Error Data too long for column 'name'
    country = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.country})"


# Таблица виробників
class Manufacturer(models.Model):
    name = models.TextField()  # Error Data too long for column 'name'
    country = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.country})"


# Основна таблиця ліків
class Drug(models.Model):
    id = models.AutoField(primary_key=True)  # змінюємо на AutoField
    original_id = models.CharField(max_length=50, unique=True)  # додаємо поле для збереження оригінального ID
    trade_name = models.TextField()  # замість CharField(max_length=255)
    international_name = models.TextField()  # замість CharField(max_length=255)
    form = models.TextField()
    conditions = models.TextField()  # Error importing drug: (1406, "Data too long for column 'conditions' at row 1")
    composition = models.TextField()
    pharmacotherapeutic_group = models.TextField()
    atc_code = models.CharField(max_length=50)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    drug_type = models.ForeignKey(DrugType, on_delete=models.CASCADE)
    manufacturers = models.ManyToManyField(Manufacturer, through='DrugManufacturer')


# Таблица термінів придатності
class ShelfLife(models.Model):
    drug = models.OneToOneField(Drug, on_delete=models.CASCADE, primary_key=True)
    bio_origin = models.BooleanField(default=False)
    plant_origin = models.BooleanField(default=False)
    orphan_drug = models.BooleanField(default=False)
    homeopathic = models.BooleanField(default=False)
    mnn_type = models.BooleanField(default=False)
    manual_url = models.TextField(null=True, blank=True)
    shelf_life = models.TextField(null=True, blank=True)
    shelf_life_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shelf_life_unit = models.CharField(max_length=50, null=True, blank=True)


# Зв'язкова таблиця між ліками та виробниками
class DrugManufacturer(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('drug', 'manufacturer')
