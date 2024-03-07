from django import forms
from common.forms import ProductAdminForm
from deciduous.models import DecProduct, DecSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm, ShelterWinterAdminForm
from plants.models import PlantGenus


class DecProductBatchCopyAdminForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    scientific_name_chk = forms.BooleanField(
        required=False, initial=True, label='Научное название')

    advantages_chk = forms.BooleanField(
        required=False, initial=True, label='Достоинства')

    height_chk = forms.BooleanField(
        required=False, initial=True, label='Высота взрослого растения')

    width_chk = forms.BooleanField(
        required=False, initial=True, label='Ширина взрослого растения')

    leaves_chk = forms.BooleanField(
        required=False, initial=True, label='Листва')

    crown_chk = forms.BooleanField(
        required=False, initial=True, label='Крона')

    flowering_chk = forms.BooleanField(
        required=False, initial=True, label='Цветение')

    flowering_period_chk = forms.BooleanField(
        required=False, initial=True, label='Период цветения')

    flower_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер цветка')

    inflorescence_chk = forms.BooleanField(
        required=False, initial=True, label='Соцветие')

    inflorescence_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер соцветия')

    planting_chk = forms.BooleanField(
        required=False, initial=True, label='Место посадки')

    shelter_winter_chk = forms.BooleanField(
        required=False, initial=True, label='Укрытие на зиму')

    winter_zone_chk = forms.BooleanField(
        required=False, initial=True, label='Зона зимостойкости')

    object_donor = forms.ModelChoiceField(
        queryset=DecProduct.objects.all(),
        label='Копировать из',
        required=True,
    )


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
