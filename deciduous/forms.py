from django import forms
from common.forms import ProductAdminForm
from deciduous.models import DecProduct, DecSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm
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
                          ProductAdminForm):
    
    CHOICES_SHELTER_WINTER = (
        (None, '---------'),
        ('обязательно', 'обязательно'),
        ('рекомендуется', 'рекомендуется'),
        ('первые 2 года', 'первые 2 года'),
    )
    shelter_winter = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_SHELTER_WINTER,
        required=False,
        label='Укрытие на зиму',
    )

    class Meta(ProductAdminForm.Meta):
        model = DecProduct
        exclude = []
