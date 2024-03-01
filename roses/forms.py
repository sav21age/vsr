from django import forms
from common.forms import ProductAdminForm
from plants.forms import PlantWinterZoneAdminForm, ShelterWinterAdminForm
from plants.models import PlantGenus
from roses.models import RoseProduct, RoseSpecies


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['winter_zone'].widget.attrs['style'] = 'width: 150px;'

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
