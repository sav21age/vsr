from django import forms
from common.forms import ProductAdminForm
from deciduous.models import DecProduct, DecSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm, ShelterWinterAdminForm
from plants.models import PlantGenus


class DecSpeciesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genus'].queryset = PlantGenus.objects.filter(
            division__name='DEC')

    class Meta:
        model = DecSpecies
        exclude = []


class DecProductAdminForm(PlantPlantingAdminForm, PlantWinterZoneAdminForm,
                          ProductAdminForm, ShelterWinterAdminForm):
    
    class Meta(ProductAdminForm.Meta):
        model = DecProduct
        exclude = []
