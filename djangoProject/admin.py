from django.contrib import admin
from .models import Drug, DrugType, Applicant, Manufacturer, ShelfLife

admin.site.register(Drug)
admin.site.register(DrugType)
admin.site.register(Applicant)
admin.site.register(Manufacturer)
admin.site.register(ShelfLife)