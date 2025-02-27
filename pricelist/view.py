from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from pricelist.models import PriceList


def price_list(request):

    try:
        obj = PriceList.objects.get()
    except ObjectDoesNotExist as e:
        raise Http404 from e

    response = render(
        request,
        'pricelist/index.html',
        {
            'object': obj,
        }
    )
    return response
