import random
from django.shortcuts import render
from common.loggers import logger
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from index.models import Index
from perennials.models import PerProduct


ON_PAGE = 2


def index(request):
    obj = Index.objects.get()

    qs_con = ConiferProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_con)
    con = []
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_con = ConiferProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('coniferproductprice_set')
        con = list(qs_con)
        random.shuffle(con)
        con = con[:ON_PAGE]
    except Exception as e:
        logger.error(e)

    qs_dec = DecProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_dec)
    dec = []
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_dec = DecProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('decproductprice_set')
        dec = list(qs_dec)
        random.shuffle(dec)
        dec = dec[:ON_PAGE]
    except Exception as e:
        logger.error(e)

    # qs_fru = FruitProduct.is_visible_objects.values_list('id', flat=True)
    # lst = list(qs_fru)
    # fru = []
    # try:
    #     lst = random.sample(lst, ON_PAGE)
    #     qs_fru = FruitProduct.is_visible_objects.filter(id__in=lst) \
    #         .prefetch_related('images') \
    #         .prefetch_related('fruitproductprice_set')
    #     fru = list(qs_fru)
    #     random.shuffle(fru)
    #     fru = fru[:4]
    # except Exception as e:
    #     logger.error(e)

    qs_per = PerProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_per)
    per = []
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_per = PerProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('perproductprice_set')
        per = list(qs_per)
        random.shuffle(per)
        per = per[:3]
    except Exception as e:
        logger.error(e)

    response = render(
        request,
        'index/index.html',
        {
            'object': obj,
            'con': con,
            'dec': dec,
            # 'fru': fru,
            'per': per,
        }
    )
    
    return response
