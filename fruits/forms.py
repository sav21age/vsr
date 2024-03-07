from django import forms
from common.forms import ProductAdminForm
from fruits.models import FruitProduct, FruitSpecies
from plants.models import PlantGenus


class FruitProductBatchCopyAdminForm(forms.Form):
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

    rootstock_chk = forms.BooleanField(
        required=False, initial=True, label='Подвой')

    fruit_ripening_chk = forms.BooleanField(
        required=False, initial=True, label='Время созревания плодов')

    fruit_taste_chk = forms.BooleanField(
        required=False, initial=True, label='Вкус плодов')

    fruit_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер плодов')

    fruit_keeping_quality_chk = forms.BooleanField(
        required=False, initial=True, label='Лежкость плодов')

    beginning_fruiting_chk = forms.BooleanField(
        required=False, initial=True, label='Начало плодоношения у растения')

    object_donor = forms.ModelChoiceField(
        queryset=FruitProduct.objects.all(),
        label='Копировать из',
        required=True,
    )


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
