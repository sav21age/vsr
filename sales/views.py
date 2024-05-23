from django.shortcuts import render
from sales.models import Discount, Promotion
# from itertools import chain


def sales(request):
    qs_d = Discount.objects.all()
    # qs_d = Discount.objects.none()
    qs_p = Promotion.objects.prefetch_related('images', 'promotionitem_set')
    # qs_p = Promotion.objects.none()

    # object_list = sorted(
    #     chain(qs_d, qs_p),
    #     key=lambda data: data.date_from, reverse=False)
    
    response = render(
        request,
        'sales/index.html',
        {
            # 'object_list': object_list,
            'qs_d': qs_d,
            'qs_p': qs_p,
        }
    )

    return response
