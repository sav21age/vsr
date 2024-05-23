from django import template

register = template.Library()


@register.filter
def month_genitive(obj):
    month_list = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря',
    ]

    return month_list[obj.month-1]
