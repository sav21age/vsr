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
from conifers.models import ConiferProduct, ConiferProductPrice, ConiferSpecies
from plants.forms import PlantPlantingAdminForm, PlantWinterZoneAdminForm
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem


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


class ConiferProductPriceFilterForm(forms.Form):
    qs = ConiferProductPrice.objects.all()

    genus = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        # widget=forms.RadioSelect(),
        queryset=PlantGenus.objects.filter(division__name='CON'),
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

    width_from = forms.IntegerField(
        label='ширина от, см.',
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
        height = ConiferProductPrice.objects.aggregate(Min('height_from'), Max('height_from'))
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

        # --

        width = ConiferProductPrice.objects.aggregate(Min('width_from'), Max('width_from'))
        width_from_min = width['width_from__min']
        width_from_max = width['width_from__max']

        self.fields['width_from'].widget = forms.NumberInput(
            attrs={
                'min': width_from_min,
                'data-min': width_from_min,
                'max': width_from_max,
                'data-max': width_from_max,
                'step': 5,
            }
        )

        self.fields['width_from'].validators.append(MinValueValidator(width_from_min))
        self.fields['width_from'].validators.append(MaxValueValidator(width_from_max))
        self.fields['width_from'].widget.attrs['placeholder'] = f"от {width_from_min} до {width_from_max}"

        #--

        self.helper = FormHelper()
        self.helper.form_id = 'coniferFilterForm'
        self.helper.form_method = 'GET'
        self.helper.form_action = reverse('conifers:list')

        self.helper.layout = Layout(
            # HTML('<div class="overlay"><div class="overlay-table"><div class="overlay-table-cell"><i class="fas fa-sync-alt fa-2x fa-spin"></i></div></div></div>'),
            HTML('<div class="overlay"><div class="overlay-table"><div class="overlay-table-cell"><i class="fas fa-spinner fa-2x fa-spin"></i></div></div></div>'),
            Div(
                # Field('genus', css_class=' col-12 d-inline-flex fix-checkbox-label'),
                InlineCheckboxes('genus'),
                css_class='row'
            ),
            Div(
                Div(
                    PrependedText(
                        'height_from', mark_safe('<i class="fas fa-ruler-vertical"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                # Div(
                #     PrependedText(
                #         'height_to', mark_safe('<i class="fas fa-ruler-vertical"></i>')),
                #     css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                # ),
                Div(
                    PrependedText(
                        'width_from', mark_safe('<i class="fas fa-ruler-horizontal"></i>')),
                    css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                ),
                # Div(
                #     PrependedText(
                #         'width_to', mark_safe('<i class="fas fa-ruler-horizontal"></i>')),
                #     css_class='col-6 col-sm-4 col-md-3 col-lg-2'
                # ),
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
                    HTML(f'<a class="btn btn-danger" href="{reverse("conifers:list")}">Сбросить</a>'),
                    css_class='col-12'
                ),
                css_class='row mb-4'
            )
        )
