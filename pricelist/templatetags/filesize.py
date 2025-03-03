from django import template

register = template.Library()

@register.filter
def get_filesize(num):
    """
    Convert bytes to KB... MB... GB... etc
    """
    lst = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']

    try:
        num = int(num)
    except ValueError:
        return '0 Б'

    if num < 0:
        return '0 Б'

    try:
        for value in lst:
            if num < 1024.0:
                if value in lst[:2]:
                    return f"{num:.0f} {value}"
                return f"{num:.1f} {value}"

            num /= 1024.0
    except:
        return '0 Б'
