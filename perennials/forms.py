from django import forms
from common.forms import ProductAdminForm
from perennials.models import PerProduct, PerSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm
from plants.models import PlantGenus


class PerSpeciesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genus'].queryset = PlantGenus.objects.filter(
            division__name='PER')

    class Meta:
        model = PerSpecies
        exclude = []


class PerProductAdminForm(PlantPlantingAdminForm, PlantWinterZoneAdminForm, 
                          ProductAdminForm):
    
    CHOICES_FLOWERING = (
        (None, '---'),
        ('обильное', 'обильное'),
        ('повторное', 'повторное'),
    )
    flowering = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_FLOWERING, 
        required=False,
        label='Цветение',
    )

    class Meta(ProductAdminForm.Meta):
        model = PerProduct
        exclude = []
