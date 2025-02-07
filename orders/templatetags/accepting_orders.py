from django import template
from orders.models import AcceptingOrders


register = template.Library()


@register.simple_tag()
def get_accepting_orders():
    try:
        obj = AcceptingOrders.objects.get()
        return obj.name
    except:
        return 'YES'
