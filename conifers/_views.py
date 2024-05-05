from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Min, Max
from common.mixins import PerPageMixin, RecommendedDetailMixin
from conifers.forms import ConiferProductPriceFilterForm
from conifers.models import ConiferProduct, ConiferProductPrice, ConiferSpecies
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem
from pure_pagination.mixins import PaginationMixin


class ConiferProductDetail(RecommendedDetailMixin, DetailView):
    model = ConiferProduct
    template_name = 'conifers/detail.html'
    queryset = ConiferProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container') \
        .prefetch_related('prices__rs')


class ConiferFilterFormMixin():
    def get_queryset(self):
        queryset = super().get_queryset()

        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data

            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                queryset = queryset.filter(species__genus__in=id_list)

            # --

            if clean['height_from']:
                queryset = queryset.filter(
                    prices__height_from__gte=clean['height_from'])

            # if clean['height_to']:
            #     queryset = queryset.filter(
            #         prices__height_to__lte=clean['height_to'])

            if clean['width_from']:
                queryset = queryset.filter(
                    prices__width_from__gte=clean['width_from'])

            # if clean['width_to']:
            #     queryset = queryset.filter(
            #         prices__width_to__lte=clean['width_to'])

            # --

            if clean['container']:
                queryset = queryset.filter(
                    prices__container=clean['container'])

            if clean['rs']:
                queryset = queryset.filter(prices__rs=clean['rs'])

            if clean['shtamb']:
                queryset = queryset.filter(prices__shtamb__regex=r"\S")
                # queryset = queryset.filter(~Q(prices__shtamb=''))

            if clean['extra']:
                queryset = queryset.filter(prices__extra=True)

            return queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = ConiferProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],

                    'height_from': clean['height_from'],
                    # 'height_to': clean['height_to'],
                    'width_from': clean['width_from'],
                    # 'width_to': clean['width_to'],

                    'container': clean['container'],
                    'rs': clean['rs'],
                    'shtamb': clean['shtamb'],
                    'extra': clean['extra'],

                    'per_page': clean['per_page'],
                },
            )
        else:
            context['form'] = ConiferProductPriceFilterForm()
        return context


class ConiferProductList(PaginationMixin,
                         ConiferFilterFormMixin,
                         PerPageMixin,
                         #  PlantSpeciesFilterMixin, PlantGenusFilterMixin,
                         ListView):
    model = ConiferProduct
    template_name = 'conifers/list.html'
    queryset = ConiferProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('prices')
    division_name = 'CON'
    species_model = ConiferSpecies


# def get_fields(fields, qs, ignore_field):

#     if ignore_field != 'genus':
#         # print(qs)
#         _qs = PlantGenus.objects.filter(coniferspecies__coniferproduct__id__in=qs)
#         print(_qs)
#         # _qs_tmp = PlantGenus.objects.filter(division__name='CON').filter(coniferspecies__coniferproduct__id__in=qs)
#         # print(_qs_tmp)
#         fields['genus'] = _qs if not fields['genus'] else fields['genus'] | _qs

# #    if field_to_ignore != 'b':
# #        _qs = Brand.objects.exclude(wristwatch__id__in=qs).distinct()
# #        fields['b'] = _qs if not fields['b'] else fields['b'] | _qs

#     if ignore_field != 'height_from':
#         fields['height_from'] = ConiferProductPrice.objects.filter(id__in=qs)\
#             .aggregate(height_from_min=Min('height_from'), height_from_max=Max('height_from'))

#     if ignore_field != 'width_from':
#         fields['width_from'] = ConiferProductPrice.objects.filter(id__in=qs)\
#             .aggregate(width_from_min=Min('width_from'), width_from_max=Max('width_from'))

# #     if field_to_ignore != 'case_w_min':
# #         fields['case_w_min'] = WristWatch.objects.filter(id__in=qs).aggregate(case_w_min=Min('case_w'))
# #
# #     if field_to_ignore != 'trbn':
# #         _qs = qs.filter(trbn=True).distinct()
# #         # _qs = WristWatch.objects.filter(id__in=qs).distinct()
# #         fields['trbn'] = True if _qs else False

#     return fields


def filter_form(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    data = {}

    form = ConiferProductPriceFilterForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data

        # if clean['genus']:
        #     id_list = list(clean['genus'].values_list('id', flat=True))
        #     qs = ConiferProductPrice.objects.filter(product__species__genus__in=id_list)
        #     fields = get_fields(fields, qs, 'genus')

        # # if clean['b']:
        # #     id_list = list(clean['b'].values_list('id', flat=True))
        # #     qs = WristWatch.is_visible_objects.filter(brand__in=id_list)
        # #     dct = get_qs(qs, dct, 'b')

        # if clean['height_from']:
        #     qs = ConiferProductPrice.objects.filter(height_from__gte=clean['height_from'])
        #     fields = get_fields(fields, qs, 'height_from')

        # if clean['width_from']:
        #     qs = ConiferProductPrice.objects.filter(width_from__gte=clean['width_from'])
        #     fields = get_fields(fields, qs, 'width_from')

        # # if clean['case_w_min']:
        # #     num = clean['case_w_min']
        # #     qs = WristWatch.is_visible_objects.filter(case_w__gte=num)
        # #     dct = get_qs(qs, dct, 'case_w')
        # #
        # # if clean['case_w_max']:
        # #     num = clean['case_w_max']
        # #     qs = WristWatch.is_visible_objects.filter(case_w__lte=num)
        # #     dct = get_qs(qs, dct, 'case_w')

        queryset = ConiferProduct.is_visible_objects.all()\
            .prefetch_related('images') \
            .prefetch_related('advantages') \
            .prefetch_related('prices') \
            .prefetch_related('prices__container') \
            .prefetch_related('prices__rs')

        if clean['genus']:
            id_list = list(clean['genus'].values_list('id', flat=True))
            print(id_list)
            queryset = queryset.filter(species__genus__in=id_list)
            print(queryset)

        if clean['height_from']:
            queryset = queryset.filter(
                prices__height_from__gte=clean['height_from'])

        if clean['width_from']:
            queryset = queryset.filter(
                prices__width_from__gte=clean['width_from'])

        if clean['container']:
            queryset = queryset.filter(
                prices__container=clean['container'])

        if clean['rs']:
            queryset = queryset.filter(prices__rs=clean['rs'])

        if clean['shtamb']:
            queryset = queryset.filter(prices__shtamb__regex=r"\S")
            # queryset = queryset.filter(~Q(prices__shtamb=''))

        if clean['extra']:
            queryset = queryset.filter(prices__extra=True)

        queryset = queryset.distinct()

        fields = {
            'genus': PlantGenus.objects.none(),

            # 'qs_b': Brand.objects.none(),
            'height_from': {},
            'width_from': {},
            # 'dct_case_w': {},
            # 'bool_trbn': None,
        }

        # print(queryset)
        id_list = list(queryset.values_list('id', flat=True))

        if clean['genus']:
            fields['genus'] = PlantGenus.objects\
                .filter(coniferspecies__coniferproduct__id__in=id_list).distinct()

        # fields['genus'] = PlantGenus.objects\
        #     .filter(coniferspecies__coniferproduct__id__in=queryset).distinct()

        # fields['height_from'] = ConiferProductPrice.objects.filter(product__in=queryset)\
        #     .aggregate(height_from_min=Min('height_from'), height_from_max=Max('height_from'))

        # fields['width_from'] = ConiferProductPrice.objects.filter(product__in=queryset)\
        #     .aggregate(width_from_min=Min('width_from'), width_from_max=Max('width_from'))

        # fields['container'] = PlantPriceContainer.objects\
        #     .filter(coniferproductprice__product_id__in=queryset).distinct()

        # fields['rs'] = PlantPriceRootSystem.objects\
        #     .filter(coniferproductprice__product_id__in=queryset).distinct()

        fields['height_from'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .aggregate(height_from_min=Min('height_from'), height_from_max=Max('height_from'))

        fields['width_from'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .aggregate(width_from_min=Min('width_from'), width_from_max=Max('width_from'))

        fields['container'] = PlantPriceContainer.objects\
            .filter(coniferproductprice__product_id__in=id_list).distinct()

        fields['rs'] = PlantPriceRootSystem.objects\
            .filter(coniferproductprice__product_id__in=id_list).distinct()

        fields['shtamb'] = ConiferProductPrice.objects.filter(product_id__in=id_list).exclude(shtamb='')\
            .order_by('shtamb').distinct('shtamb').values_list('shtamb', flat=True)

        print(fields['shtamb'])

        fields['extra'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .order_by('extra').distinct('extra').values_list('extra', flat=True)

        print(fields['extra'])

        data.update(
            {'genus': list(fields['genus'].values_list('id', flat=True))})
        # data.update({'b': list(dct['qs_b'].values_list('id', flat=True))})
        data.update({'height_from': fields['height_from']})
        data.update({'width_from': fields['width_from']})
        data.update(
            {'container': list(fields['container'].values_list('id', flat=True))})
        data.update({'rs': list(fields['rs'].values_list('id', flat=True))})
        # data.update({'case_w': dct['dct_case_w']})
        data.update({'extra': [] if True in fields['extra'] else None})
        data.update({'shtamb': [] if not fields['shtamb'] else None})
        # print(data)

    return JsonResponse(data)
