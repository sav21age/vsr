from django import forms
from django.forms import Textarea
from common.models import Product
from plants.models import PlantDivision, PlantGenius, PlantGroup
from django_select2.forms import ModelSelect2Widget
from common.helpers import codemirror_widget
from codemirror import CodeMirrorTextarea

# # class PageAdminForm(forms.ModelForm):
# #     class Meta:
# #         model = Page
# #         widgets = {
# #             'meta_description': Textarea(
# #                 attrs={'rows': 3, 'style': 'width: 70%; font-size: 115%;'}),
# #         }
# #         exclude = []


class ProductAdminForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=PlantDivision.objects.all(),
        label="Отдел",
        widget=ModelSelect2Widget(
            search_fields=['name__icontains'],
            attrs={
                "data-minimum-input-length": 0,
            }            
        ),
        required=False,
    )

    genius = forms.ModelChoiceField(
        queryset=PlantGenius.objects.all(),
        label="Род",
        widget=ModelSelect2Widget(
            search_fields=['name__icontains'],
            dependent_fields={'division': 'division'},
            attrs={
                "data-minimum-input-length": 0,
            },
            max_results=100,
        ),
        required=False,
    )

    class Meta:
        # description = forms.CharField(
        #     label='Описание!', required=False, widget=codemirror_widget)
        
        model = Product
        widgets = {
            'meta_description': Textarea(
                attrs={'rows': 3, 'style': 'width: 70%; font-size: 115%;'}),
            # 'description': Textarea(
            #     attrs={'style': 'width: 70%; font-size: 115%;'}),

            'description': CodeMirrorTextarea(
                    mode="markdown",
                    # theme="eclipse",
                    # theme="neo",
                    config={
                        'fixedGutter': True,
                        'lineWrapping': True,
                        'matchBrackets': True,
                    },
                ),
            
            # 'division': ModelSelect2Widget(
            #     model=PlantDivision, 
            #     label="Отдел",
            #     search_fields=['name__icontains'],
            #     attrs={
            #         "data-minimum-input-length": 0,
            #         # "data-placeholder": "Select an option",
            #         # "data-close-on-select": "false",
            #     }
            #     ),
            # 'genius': ModelSelect2Widget(
            #     model=PlantGenius,
            #     label="Род",
            #     # queryset=PlantGenius.objects.all(),
            #     search_fields=['name__icontains'],
            #     dependent_fields={'division': 'division'},
            #     attrs={
            #         "data-minimum-input-length": 0,
            #     }
            #     ),
            'group': ModelSelect2Widget(
                model=PlantGroup,
                label="Группа",
                # queryset=PlantGroup.objects.all(),
                search_fields=['name__icontains'],
                dependent_fields={'genius': 'genius'},
                attrs={
                    "data-minimum-input-length": 0,
                }
            ),
        }
        exclude = []
