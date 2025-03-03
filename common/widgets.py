from codemirror import CodeMirrorTextarea
from django.db import models
from django.forms import NumberInput, Textarea, TextInput


textarea_widget = Textarea(attrs={'rows': 3, 'style': 'width: 70%; font-size: 115%;'})

codemirror_widget = CodeMirrorTextarea(
    mode="markdown",
    config={
        'fixedGutter': True,
        'lineWrapping': True,
        'matchBrackets': True,
    },
)

formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'style': 'width: 75%; font-size: 120%; height: 18px;'})},
    models.DecimalField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 120%;'})},
    # models.SelectField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 115%;'})},
    # ThumbnailerImageField:{'widget': ImageAdminWidget(),},
    # models.TextField: {'widget': Textarea(attrs={'rows': 30, 'style': 'width: 70%; font-size: 115%;'})},
    # models.TextField: {'widget': codemirror_widget},
    # models.IntegerField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 115%;'})},
}
