from django import forms
from common.forms import ProductAdminForm
from perennials.models import PerProduct, PerSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm
from plants.models import PlantGenus


class PerProductBatchCopyAdminForm(forms.Form):
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

    flowering_chk = forms.BooleanField(
        required=False, initial=True, label='Цветение')

    flowering_duration_chk = forms.BooleanField(
        required=False, initial=True, label='Продолжительность цветения')

    flowering_period_chk = forms.BooleanField(
        required=False, initial=True, label='Период цветения')

    flower_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер цветка')

    inflorescence_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер соцветия')

    planting_chk = forms.BooleanField(
        required=False, initial=True, label='Место посадки')

    winter_zone_chk = forms.BooleanField(
        required=False, initial=True, label='Зона зимостойкости')

    object_donor = forms.ModelChoiceField(
        queryset=PerProduct.objects.all(),
        label='Копировать из',
        required=True,
    )


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
