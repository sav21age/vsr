from django import forms
from plants.models import PlantPlanting

# from django.forms import Textarea
# from common.models import Product
# from plants.models import PlantDivision, PlantGenius, PlantGroup
# from django_select2.forms import ModelSelect2Widget
# from common.helpers import codemirror_widget
# from codemirror import CodeMirrorTextarea


# class PlantGeniusAdminForm(forms.ModelForm):
#     division = forms.ModelChoiceField(
#         queryset=PlantDivision.objects.all(),
#         label="Отдел",
#         widget=ModelSelect2Widget(
#             search_fields=['name__icontains'],
#             attrs={
#                 "data-minimum-input-length": 0,
#             }
#         ),
#         required=False,
#     )


# class PlantPlantingFieldAbstractAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['planting'].widget.attrs['style'] = 'width: 100px;'



class PlantPlantingAdminForm(forms.ModelForm):
    planting = forms.ModelMultipleChoiceField(
        queryset=PlantPlanting.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            # attrs={'class': 'inline'}
        ),
        required=False,
        label='Место посадки',
    )

class PlantWinterZoneAdminForm(forms.ModelForm):
    CHOICES_WINTER_ZONE = (
        (None, '---------'),
        ('6 (-23)', '6 (-23)'),
        ('5 (-29)', '5 (-29)'),
        ('4 (-34)', '4 (-34)'),
        ('3 (-40)', '3 (-40)'),
    )
    winter_zone = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        choices=CHOICES_WINTER_ZONE, 
        required=False,
        label='Зона зимостойкости в градусах',
    )
    

class ShelterWinterAdminForm(forms.ModelForm):
    CHOICES_SHELTER_WINTER = (
        (None, '---------'),
        ('обязательно', 'обязательно'),
        ('рекомендуется первые 2 года', 'рекомендуется первые 2 года'),
        ('не требуется', 'не требуется'),
    )
    shelter_winter = forms.ChoiceField(
        widget=forms.Select(attrs={'style': 'width: 200px;'}),
        choices=CHOICES_SHELTER_WINTER,
        required=False,
        label='Укрытие на зиму',
    )
    
    # class Media:
    #     css = {"all": ("assets/admin.css",)}
    # https://stackoverflow.com/a/77124464/4095667