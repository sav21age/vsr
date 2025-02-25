from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from orders.models import AcceptingOrders
from pricelist.models import PriceList


def price_list(request):
    try:
        obj = AcceptingOrders.objects.get()
        accepting_orders = obj.name
    except:
        accepting_orders = 'ORDER'

    try:
        obj = PriceList.objects.get()
    except ObjectDoesNotExist as e:
        raise Http404 from e

    response = render(
        request,
        'pricelist/index.html',
        {
            'object': obj,
            'accepting_orders': accepting_orders,
        }
    )
    return response
