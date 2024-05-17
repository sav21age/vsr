from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from crispy_forms.bootstrap import PrependedText, InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import Switch
from common.forms import ProductAdminForm
from perennials.models import PerProductFlowering, PerProduct, PerProductPrice, PerSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm, ShelterWinterAdminForm
from plants.models import PlantGenus, PlantPriceContainer


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

    shelter_winter_chk = forms.BooleanField(
        required=False, initial=True, label='Укрытие на зиму')

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
                          ShelterWinterAdminForm, ProductAdminForm):
    
    # CHOICES_FLOWERING = (
    #     (None, '---'),
    #     ('обильное', 'обильное'),
    #     ('повторное', 'повторное'),
    #     ('продолжительное', 'продолжительное'),
    # )
    # flowering = forms.ChoiceField(
    #     widget=forms.Select(attrs={'style': 'width: 150px;'}),
    #     choices=CHOICES_FLOWERING, 
    #     required=False,
    #     label='Цветение',
    # )
    flowering = forms.ModelMultipleChoiceField(
        queryset=PerProductFlowering.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            # attrs={'class': 'inline'}
        ),
        required=False,
        label='Цветение',
    )

    class Meta(ProductAdminForm.Meta):
        model = PerProduct
        exclude = []


class PerProductPriceFilterForm(forms.Form):
    qs = PerProductPrice.objects.all()

    genus = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=PlantGenus.objects.filter(division__name='PER'),
        # queryset=PlantGenus.objects.filter(
        #     perspecies__perproduct__id__in=qs.values_list('product', flat=True).order_by('product_id').distinct('product')).distinct(),
        label='',
        required=False
    )

    container = forms.ModelChoiceField(
        widget=forms.Select(),
        # queryset=PlantPriceContainer.objects.all(),
        queryset=PlantPriceContainer.objects.filter(
            id__in=qs.values_list('container', flat=True).order_by('container_id').distinct('container')),
        label='контейнер:',
        required=False
    )

    planting_year = forms.ChoiceField(
        # widget=forms.Select(),
        # queryset=qs.exclude(planting_year='').values_list(
        #     'planting_year', flat=True).order_by('planting_year').distinct('planting_year'),
        label='год посадки:',
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

        CHOICES = [('', '---------')] + [(choice, choice) for choice in PerProductPrice.objects.exclude(planting_year='').values_list(
                'planting_year', flat=True).order_by('planting_year').distinct('planting_year')
        ]

        self.fields['planting_year'].choices = CHOICES

        #--

        self.helper = FormHelper()
        self.helper.form_id = 'perFilterForm'
        self.helper.form_method = 'GET'
        self.helper.form_action = reverse('pers:list')

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
                        'planting_year', mark_safe('<i class="far fa-calendar-check"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('per_page', type="hidden"),
                    Field('show_filters', type="hidden"),
                    HTML('<button class="btn btn-tertiary me-4">Фильтровать</button>'),
                    HTML(
                        f'<a class="btn btn-danger" href="{reverse("pers:list")}">Сбросить</a>'),
                    css_class='col-12'
                ),
                css_class='row mb-4'
            )
        )
