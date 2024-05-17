from django import forms
from django.db.models import Min, Max
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from crispy_forms.bootstrap import PrependedText, InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import Switch
from common.forms import ProductAdminForm
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm, ShelterWinterAdminForm
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem


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


class DecProductPriceFilterForm(forms.Form):
    qs = DecProductPrice.objects.all()

    genus = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        # widget=forms.RadioSelect(),
        queryset=PlantGenus.objects.filter(division__name='DEC'),
        label='',
        # label='Род растений',
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

    rs = forms.ModelChoiceField(
        widget=forms.Select(),
        # queryset=PlantPriceRootSystem.objects.all(),
        queryset=PlantPriceRootSystem.objects.filter(
            id__in=qs.values_list('rs', flat=True).order_by('rs_id').distinct('rs')),
        label='корневая система:',
        required=False
    )

    shtamb = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='штамб',
        required=False,
    )

    extra = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='экстра',
        required=False,
    )

    height_from = forms.IntegerField(
        label='высота от, см.',
        required=False,
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
        height = DecProductPrice.objects.aggregate(Min('height_from'), Max('height_from'))
        height_from_min = height['height_from__min']
        height_from_max = height['height_from__max']

        self.fields['height_from'].widget = forms.NumberInput(
            attrs={
                'min': height_from_min,
                'data-min': height_from_min,
                'max': height_from_max,
                'data-max': height_from_max,
                'step': 5,
            }
        )

        self.fields['height_from'].validators.append(MinValueValidator(height_from_min))
        self.fields['height_from'].validators.append(MaxValueValidator(height_from_max))
        self.fields['height_from'].widget.attrs['placeholder'] = f"от {height_from_min} до {height_from_max}"

        #--

        self.helper = FormHelper()
        self.helper.form_id = 'decFilterForm'
        self.helper.form_method = 'GET'
        self.helper.form_action = reverse('decs:list')

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
                        'height_from', mark_safe('<i class="fas fa-ruler-vertical"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
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
                    Switch('shtamb'),
                    # Field('shtamb', css_class="form-check-input",
                    #       wrapper_class="form-check form-switch mb-2"),
                    Switch('extra'),
                    css_class='col-6 col-sm-2'
                ),
                # Div(
                #     # Field('extra'),
                #     Switch('extra'),
                #     css_class='col-6 col-sm-2'
                # ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('per_page', type="hidden"),
                    Field('show_filters', type="hidden"),
                    # Switch('show_filters', type="hidden"),
                    HTML('<button class="btn btn-tertiary me-4">Фильтровать</button>'),
                    HTML(
                        f'<a class="btn btn-danger" href="{reverse("decs:list")}">Сбросить</a>'),
                    css_class='col-12'
                ),
                css_class='row mb-4'
            )
        )
