from django import forms
from common.forms import ProductAdminForm
from plants.forms import PlantWinterZoneAdminForm, ShelterWinterAdminForm
from roses.models import RoseProduct, RoseSpecies


class RoseProductBatchCopyAdminForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    scientific_name_chk = forms.BooleanField(
        required=False, initial=True, label='Научное название')

    advantages_chk = forms.BooleanField(
        required=False, initial=True, label='Достоинства')

    height_chk = forms.BooleanField(
        required=False, initial=True, label='Высота взрослого растения')

    width_chk = forms.BooleanField(
        required=False, initial=True, label='Ширина взрослого растения')

    flowering_chk = forms.BooleanField(
        required=False, initial=True, label='Цветение')
    
    quantity_on_stem_chk = forms.BooleanField(
        required=False, initial=True, label='Количество на стебле')

    flavor_chk = forms.BooleanField(
        required=False, initial=True, label='Аромат')

    flower_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер цветка')

    resistance_fungus_chk = forms.BooleanField(
        required=False, initial=True, label='Устойчивость к грибковым инфекциям')

    resistance_rain_chk = forms.BooleanField(
        required=False, initial=True, label='Устойчивость к дождю')

    shelter_winter_chk = forms.BooleanField(
        required=False, initial=True, label='Укрытие на зиму')

    winter_zone_chk = forms.BooleanField(
        required=False, initial=True, label='Зона зимостойкости')

    object_donor = forms.ModelChoiceField(
        queryset=RoseProduct.objects.all(),
        label='Копировать из',
        required=True,
    )


class RoseSpeciesAdminForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['genus'].queryset = PlantGenus.objects.filter(
    #         name='Роза')

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    class Meta:
        model = RoseSpecies
        exclude = []


class RoseProductAdminForm(PlantWinterZoneAdminForm, ShelterWinterAdminForm, ProductAdminForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['winter_zone'].widget.attrs['style'] = 'width: 150px;'

    CHOICES_FLOWERING = (
        (None, '---------'),
        ('однократное', 'однократное'),
        ('повторное', 'повторное'),
        ('непрерыноцветущая', 'непрерыноцветущая'),
    )
    flowering = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 200px;'}),
        choices=CHOICES_FLOWERING,
        required=False,
        label='Цветение',
    )

    CHOICES_FLAVOR = (
        (None, '---------'),
        ('слабый', 'слабый'),
        ('средний', 'средний'),
        ('сильный', 'сильный'),
    )
    flavor = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_FLAVOR,
        required=False,
        label='Аромат',
    )

    CHOICES_LMS = (
        (None, '---------'),
        ('низкая', 'низкая'),
        ('средняя', 'средняя'),
        ('высокая', 'высокая'),
    )
    resistance_fungus = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_LMS,
        required=False,
        label='Устойчивость к грибковым инфекциям',
    )
    resistance_rain = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_LMS,
        required=False,
        label='Устойчивость к дождю',
    )

    class Meta(ProductAdminForm.Meta):
        model = RoseProduct
        exclude = []
