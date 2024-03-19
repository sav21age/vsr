# from datetime import datetime
from urllib.parse import urljoin
from django.conf import settings
# from django.core.files.storage import FileSystemStorage
import os
from django.forms import NumberInput, TextInput, Textarea
from django.db import models
from codemirror import CodeMirrorTextarea
# from easy_thumbnails.fields import ThumbnailerImageField
# from images.widgets import ImageAdminWidget


codemirror_widget = CodeMirrorTextarea(
    mode="markdown",
    config={
        'fixedGutter': True,
        'lineWrapping': True,
        'matchBrackets': True,
    },
)

textarea_widget = Textarea(attrs={'rows': 3, 'style': 'width: 70%; font-size: 115%;'})

formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'style': 'width: 75%; font-size: 120%; height: 18px;'})},
    models.DecimalField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 120%;'})},
    # models.SelectField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 115%;'})},
    # ThumbnailerImageField:{'widget': ImageAdminWidget(),},
    # models.TextField: {'widget': Textarea(attrs={'rows': 30, 'style': 'width: 70%; font-size: 115%;'})},
    # models.TextField: {'widget': codemirror_widget},
    # models.IntegerField: {'widget': NumberInput(attrs={'style': 'width: 100px; font-size: 115%;'})},
}


def get_price_properties(obj):

    s = ''
    if hasattr(obj, 'container') and obj.container:
        s = f"{obj.container} "

    if (hasattr(obj, 'height') and obj.height) and (hasattr(obj, 'width') and obj.width):
        s = f"{s}{obj.height}x{obj.width} "
    else:
        if hasattr(obj, 'height') and obj.height:
            s = f"{s}{obj.height} "

        if hasattr(obj, 'width') and obj.width:
            s = f"{s}{obj.width} "

    if hasattr(obj, 'trunk_diameter') and obj.trunk_diameter:
        s = f"{s}{obj.trunk_diameter} "

    if hasattr(obj, 'shtamb') and obj.shtamb:
        # s = f"{s}{obj._meta.get_field('shtamb').verbose_name} {obj.shtamb} "
        s = f"{s} штамб {obj.shtamb} "

    if hasattr(obj, 'rs') and obj.rs:
        s = f"{s}{obj.rs} "

    if hasattr(obj, 'planting_year') and obj.planting_year:
        s = f"{s}- {obj.planting_year} г. "

    if hasattr(obj, 'extra') and obj.extra:
        s = f"{s}{obj._meta.get_field('extra').verbose_name} "

    if hasattr(obj, 'property') and obj.property:
        s = f"{s}{obj.property}"

    return s.strip()


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return f"{ip}"
