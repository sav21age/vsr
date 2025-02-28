import random
from django.http import Http404
from django.shortcuts import render
from common.loggers import logger
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from index.models import Index
from perennials.models import PerProduct


ON_PAGE = 2


def index(request):
    try:
        obj = Index.objects.get()
    except Exception as e:
        logger.error(e)
        raise Http404 from e

    qs_con = ConiferProduct.is_visible_objects.values_list('id', flat=True)
    try:
        lst = random.sample(list(qs_con), ON_PAGE)
        qs_con = ConiferProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('prices')
    except Exception as e:
        logger.error(e)
        obj.con_visible = False

    qs_dec = DecProduct.is_visible_objects.values_list('id', flat=True)
    try:
        lst = random.sample(list(qs_dec), ON_PAGE)
        qs_dec = DecProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('prices')
    except Exception as e:
        logger.error(e)
        obj.dec_visible = False

    qs_fru = FruitProduct.is_visible_objects.values_list('id', flat=True)
    try:
        lst = random.sample(list(qs_fru), ON_PAGE)
        qs_fru = FruitProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('prices')
    except Exception as e:
        logger.error(e)
        obj.fru_visible = False

    qs_per = PerProduct.is_visible_objects.values_list('id', flat=True)
    try:
        lst = random.sample(list(qs_per), ON_PAGE)
        qs_per = PerProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('prices')
    except Exception as e:
        logger.error(e)
        obj.per_visible = False

    response = render(
        request,
        'index/index.html',
        {
            'object': obj,
            'qs_con': qs_con,
            'qs_dec': qs_dec,
            'qs_fru': qs_fru,
            'qs_per': qs_per,
        }
    )

    return response
