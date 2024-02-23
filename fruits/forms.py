from django import forms
from common.forms import ProductAdminForm
from fruits.models import FruitProduct, FruitSpecies
from plants.models import PlantGenus


class FruitSpeciesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genus'].queryset = PlantGenus.objects.filter(
            division__name='FRU')

    class Meta:
        model = FruitSpecies
        exclude = []


class FruitProductAdminForm(ProductAdminForm):
    CHOICES_FLOWERING = (
        (None, '---'),
        ('раннее', 'раннее'),
        ('среднее', 'среднее'),
        ('позднее', 'позднее'),
    )
    flowering = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_FLOWERING, 
        required=False,
        label='Цветение',
    )
    
    CHOICES_FRUIT_RIPENING = (
        (None, '---'),
        ('раннее', 'раннее'),
        ('среднее', 'среднее'),
        ('позднее', 'позднее'),
        ('летнее', 'летнее'),
        ('осненнее', 'осненнее'),
        ('зимнее', 'зимнее'),
    )
    fruit_ripening = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_FRUIT_RIPENING,
        required=False,
        label='Время созревания плодов',
    )

    CHOICES_ROOTSTOCK = (
        (None, '---'),
        ('карликовый', 'карликовый'),
        ('полукарликовый', 'полукарликовый'),
    )
    rootstock = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_ROOTSTOCK,
        required=False,
        label='Подвой',
    )

    class Meta(ProductAdminForm.Meta):
        model = FruitProduct
        exclude = []
