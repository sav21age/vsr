from django import forms
from common.forms import ProductAdminForm
from conifers.models import ConiferProduct, ConiferSpecies
from plants.forms import (
    PlantPlantingAdminForm, PlantWinterZoneAdminForm)
from plants.models import PlantGenus


class ConiferProductBatchCopyAdminForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    scientific_name_chk = forms.BooleanField(
        required=False, initial=True, label='Научное название')

    advantages_chk = forms.BooleanField(
        required=False, initial=True, label='Достоинства')

    height_chk = forms.BooleanField(
        required=False, initial=True, label='Высота взрослого растения')

    width_chk = forms.BooleanField(
        required=False, initial=True, label='Ширина взрослого растения')

    needles_chk = forms.BooleanField(
        required=False, initial=True, label='Хвоя')

    height10_chk = forms.BooleanField(
        required=False, initial=True, label='Высота в 10 лет')

    width10_chk = forms.BooleanField(
        required=False, initial=True, label='Ширина в 10 лет')

    height1_chk = forms.BooleanField(
        required=False, initial=True, label='Годовой прирост в высоту')

    width1_chk = forms.BooleanField(
        required=False, initial=True, label='Годовой прирост в ширину')

    planting_chk = forms.BooleanField(
        required=False, initial=True, label='Место посадки')

    shelter_chk = forms.BooleanField(
        required=False, initial=True, label='Укрытие')

    winter_zone_chk = forms.BooleanField(
        required=False, initial=True, label='Зона зимостойкости')

    object_donor = forms.ModelChoiceField(
        queryset=ConiferProduct.objects.all(),
        label='Копировать из',
        required=True,
    )


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
