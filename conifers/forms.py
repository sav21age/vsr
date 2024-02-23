from django import forms
from common.forms import ProductAdminForm
from conifers.models import ConiferProduct, ConiferSpecies
from plants.forms import (
    PlantPlantingAdminForm, PlantWinterZoneAdminForm)
from plants.models import PlantGenus


class ConiferSpeciesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genus'].queryset = PlantGenus.objects.filter(
            division__name='CON')

    class Meta:
        model = ConiferSpecies
        exclude = []


class ConiferProductAdminForm(PlantPlantingAdminForm, PlantWinterZoneAdminForm, 
                              ProductAdminForm):

    CHOICES_SHELTER = (
        (None, '---------'),
        ('от весеннего солнца', 'от весеннего солнца'),
        ('на зиму', 'на зиму'),
    )
    shelter = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_SHELTER,
        required=False,
        label='Укрытие',
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['winter_zone'].widget.attrs['style'] = 'width: 150px;'
        
    class Meta(ProductAdminForm.Meta):
        model = ConiferProduct
        # widgets = {
        #     'species': ModelSelect2Widget(
        #         model=ConiferSpecies,
        #         label="Группа",
        #         search_fields=['name__icontains'],
        #         # dependent_fields={'genius': 'genius'},
        #         attrs={
        #             "data-minimum-input-length": 0,
        #         }
        #     )
        # }

        exclude = []
