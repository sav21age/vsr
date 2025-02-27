from pathlib import Path
from django import template

register = template.Library()


@register.filter
def get_filename(path):
    
    name = ''
    try:
        name = Path(path).name
    except:
        pass
    
    return name