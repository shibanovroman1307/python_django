from django import forms
from django.forms import inlineformset_factory
from .models import Drug, ShelfLife


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = [
            'original_id', 'trade_name', 'international_name', 'form', 'conditions',
            'composition', 'pharmacotherapeutic_group', 'atc_code', 'applicant',
            'registration_number', 'start_date', 'end_date', 'drug_type'
        ]


ShelfLifeFormSet = inlineformset_factory(
    Drug,
    ShelfLife,
    fields=[
        'bio_origin', 'plant_origin', 'orphan_drug', 'homeopathic', 'mnn_type',
        'manual_url', 'shelf_life', 'shelf_life_value', 'shelf_life_unit'
    ],
    extra=1
)
