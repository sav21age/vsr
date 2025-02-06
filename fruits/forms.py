from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from crispy_forms.bootstrap import PrependedText, InlineCheckboxes
# from crispy_bootstrap5.bootstrap5 import Switch
from common.forms import ProductAdminForm
from fruits.models import FruitProduct, FruitProductPrice, FruitProductPriceAge, FruitSpecies
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem


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

    self_fertility_chk = forms.BooleanField(
        required=False, initial=True, label='Самоплодность')

    # rootstock_chk = forms.BooleanField(
    #     required=False, initial=True, label='Подвой')

    fruit_ripening_chk = forms.BooleanField(
        required=False, initial=True, label='Время созревания плодов')

    fruit_taste_chk = forms.BooleanField(
        required=False, initial=True, label='Вкус плодов')

    fruit_dimension_chk = forms.BooleanField(
        required=False, initial=True, label='Величина плодов')

    fruit_size_chk = forms.BooleanField(
        required=False, initial=True, label='Размер плодов')

    fruit_weight_chk = forms.BooleanField(
        required=False, initial=True, label='Вес плодов')

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
        ('мелкие', 'мелкие'),
        ('средние', 'средние'),
        ('крупные', 'крупные'),
    )
    fruit_dimension = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_FLOWERING, 
        required=False,
        label='Величина плодов',
    )

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

    CHOICES_SELF_FERTILITY = (
        (None, '---'),
        ('самоплодна', 'самоплодна'),
        ('частично самоплодна', 'частично самоплодна'),
        ('самобесплодна', 'самобесплодна'),
    )
    self_fertility = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_SELF_FERTILITY,
        required=False,
        label='Самоплодность',
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

    class Meta(ProductAdminForm.Meta):
        model = FruitProduct
        exclude = []


class FruitProductPriceAdminForm(forms.ModelForm):
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

    class Meta:
        model = FruitProductPrice
        exclude = []


class FruitProductPriceFilterForm(forms.Form):
    qs = FruitProductPrice.objects.all()

    genus = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        # widget=forms.RadioSelect(),
        queryset=PlantGenus.objects.filter(division__name='FRU'),
        label='',
        # label='Род растений',
        required=False
    )

    container = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=PlantPriceContainer.objects.filter(
            id__in=qs.values_list('container', flat=True).order_by('container_id').distinct('container')),
        label='контейнер:',
        required=False
    )

    rs = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=PlantPriceRootSystem.objects.filter(
            id__in=qs.values_list('rs', flat=True).order_by('rs_id').distinct('rs')),
        label='корневая система:',
        required=False
    )

    age = forms.ModelChoiceField(
        widget=forms.Select(),
        # queryset=PlantPriceRootSystem.objects.all(),
        queryset=FruitProductPriceAge.objects.filter(
            id__in=qs.values_list('age', flat=True).order_by('age_id').distinct('age')),
        label='возраст:',
        required=False
    )

    per_page = forms.IntegerField(
        required=False,
    )

    show_filters = forms.CharField(
        # widget=forms.CheckboxInput(),
        initial='yes',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'fruitFilterForm'
        self.helper.form_method = 'GET'
        self.helper.form_action = reverse('fruits:list')

        self.helper.layout = Layout(
            # HTML('<div class="overlay"><div class="overlay-table"><div class="overlay-table-cell"><i class="fas fa-sync-alt fa-2x fa-spin"></i></div></div></div>'),
            HTML('<div class="overlay"><div class="overlay-table"><div class="overlay-table-cell"><i class="fas fa-spinner fa-2x fa-spin"></i></div></div></div>'),
            Div(
                # Field('genus', css_class=' col-12 d-inline-flex fix-checkbox-label'),
                InlineCheckboxes(
                    'genus', css_class='max-height overflow-y-auto'),
                css_class='row'
            ),
            Div(
                Div(
                    PrependedText(
                        'container', mark_safe('<i class="fas fa-archive"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                Div(
                    PrependedText(
                        'rs', mark_safe('<i class="fas fa-carrot"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                Div(
                    PrependedText(
                        'age', mark_safe('<i class="far fa-calendar"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('per_page', type="hidden"),
                    Field('show_filters', type="hidden"),
                    # Switch('show_filters', type="hidden"),
                    HTML('<button class="btn btn-tertiary me-4">Фильтровать</button>'),
                    HTML(
                        f'<a class="btn btn-danger" href="{reverse("fruits:list")}">Сбросить</a>'),
                    css_class='col-12'
                ),
                css_class='row mb-4'
            )
        )
