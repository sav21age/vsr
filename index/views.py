import random
from django.shortcuts import render
from common.loggers import logger
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from index.models import Index
from perennials.models import PerProduct


# def get_qs(model):
#     qs = model.is_visible_objects.filter(
#         is_discontinued=False).values_list('id', flat=True)
#     lst = list(qs)
#     try:
#         lst = random.sample(lst, ON_PAGE)
#         qs = model.is_visible_objects \
#             .annotate(min_price=Min('store_items__low', filter=Q(store_items__is_visible=True, store_items__low__gt=0))) \
#             .filter(store_items__is_visible=True) \
#             .filter(id__in=lst) \
#             .select_related('brand') \
#             .prefetch_related('images')
#         return qs
#     except ValueError as e:
#         logger.error(e)


# def index(request):
#     if request.user.is_authenticated:
#         qs_recently_viewed = RecentlyViewed.objects.filter(user=request.user) \
#             .prefetch_related('content_object') \
#             .prefetch_related('content_object__brand')[:ON_PAGE]
#     else:
#         qs_recently_viewed = RecentlyViewed.objects.none()

#     # ---

#     models = (WristWatch, SmartWatch, SmartWristband,)
#     yml = []
#     for model in models:
#         yml += list(get_qs(model))

#     random.shuffle(yml)

#     try:
#         yml = yml[:ON_PAGE]
#     except IndexError as e:
#         logger.error(e)
#         yml = []

#     # ---

#     date_now = datetime.today()
#     date_str_start = date_now.strftime('%Y-%m-%d')
#     date_str_end = (date_now + timedelta(days=60)).strftime('%Y-%m-%d')

#     qs = Sale.objects.prefetch_related('sites')
#     qs_s_gt = qs.filter(date_start__gt=datetime.now(),
#                         date_start__range=(date_str_start, date_str_end))
#     qs_s_e = qs.filter(date_start__lte=datetime.now(),
#                        date_end__gte=datetime.now())
#     qs_sale = qs_s_gt | qs_s_e

    # response = render(
    #     request,
    #     'index/index.html',
    #     {
    #         'brands': Brand.is_visible_objects.order_by('-count').prefetch_related('images')[:12],
    #         'yml': yml,
    #         'sale' : qs_sale,
    #         'sites': Site.is_visible_objects.order_by('netloc_en'),
    #         'recently_viewed': qs_recently_viewed,
    #         'RUB': Currency.objects.filter(abbr='RUB').latest('date'),
    #         'EUR': Currency.objects.filter(abbr='EUR').latest('date'),
    #     }
    # )
    # return response

ON_PAGE = 4

def get_qs(model):
    qs = model.is_visible_objects.values_list('id', flat=True)

    lst = list(qs)
    try:
        lst = random.sample(lst, ON_PAGE)
        
        # qs = model.is_visible_objects \
        #     .filter(id__in=lst) \
        #     .select_related('species') \
        #     .prefetch_related('images') \
            # .prefetch_related('coniferproductprice_set')

        return qs
    except ValueError as e:
        logger.error(e)


def index(request):
    obj = Index.objects.get()

    showcase = []

    qs_con = ConiferProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_con)
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_con = ConiferProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('coniferproductprice_set')
        showcase += list(qs_con)
    except ValueError as e:
        logger.error(e)

    qs_dec = DecProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_dec)
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_dec = DecProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('decproductprice_set')
        showcase += list(qs_dec)
    except ValueError as e:
        logger.error(e)

    qs_fru = FruitProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_fru)
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_fru = FruitProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('fruitproductprice_set')
        showcase += list(qs_fru)
    except ValueError as e:
        logger.error(e)

    qs_per = PerProduct.is_visible_objects.values_list('id', flat=True)
    lst = list(qs_per)
    try:
        lst = random.sample(lst, ON_PAGE)
        qs_per = PerProduct.is_visible_objects.filter(id__in=lst) \
            .prefetch_related('images') \
            .prefetch_related('perproductprice_set')
        showcase += list(qs_per)
    except ValueError as e:
        logger.error(e)

    random.shuffle(showcase)

    try:
        showcase1 = showcase[:ON_PAGE]
        showcase2 = showcase[ON_PAGE:ON_PAGE*2]
    except IndexError as e:
        logger.error(e)
        showcase1 = showcase2 = []

    response = render(
        request,
        'index/index.html',
        {
            'object': obj,
            'showcase1': showcase1,
            'showcase2': showcase2,
        }
    )
    return response
