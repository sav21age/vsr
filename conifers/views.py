from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
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
    

class ConiferFilterFormMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
    
            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                qs = qs.filter(species__genus__in=id_list)

            if clean['height_from']:
                qs = qs.filter(
                    prices__height_from__gte=clean['height_from'])

            if clean['width_from']:
                qs = qs.filter(
                    prices__width_from__gte=clean['width_from'])

            if clean['container']:
                qs = qs.filter(prices__container=clean['container'])

            if clean['rs']:
                qs = qs.filter(prices__rs=clean['rs'])

            if clean['shtamb']:
                qs = qs.filter(prices__shtamb__regex=r"\S")
                # qs = qs.filter(~Q(prices__shtamb=''))

            if clean['extra']:
                qs = qs.filter(prices__extra=True)

            return qs.distinct()
    
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = ConiferProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],
                    'height_from': clean['height_from'],
                    'width_from': clean['width_from'],
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


def filter_form(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    form = ConiferProductPriceFilterForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data

        qs = ConiferProduct.is_visible_objects.all()\
            .prefetch_related('prices') \
            .prefetch_related('prices__container') \
            .prefetch_related('prices__rs')\
            # .prefetch_related('images') \
            # .prefetch_related('advantages')

        if clean['height_from']:
            qs = qs.filter(
                prices__height_from__gte=clean['height_from'])

        if clean['width_from']:
            qs = qs.filter(
                prices__width_from__gte=clean['width_from'])

        if clean['container']:
            qs = qs.filter(
                prices__container=clean['container'])

        if clean['rs']:
            qs = qs.filter(prices__rs=clean['rs'])

        if clean['shtamb']:
            qs = qs.filter(prices__shtamb__regex=r"\S")
            # qs = qs.filter(~Q(prices__shtamb=''))

        if clean['extra']:
            qs = qs.filter(prices__extra=True)

        qs_no_genus = qs.distinct()
        id_list_no_genus = list(qs_no_genus.values_list('id', flat=True))

        if clean['genus']:
            id_list = list(clean['genus'].values_list('id', flat=True))
            qs = qs.filter(species__genus__in=id_list)

        qs = qs.distinct()
        id_list = list(qs.values_list('id', flat=True))

        fields = {}

        fields['genus'] = PlantGenus.objects\
            .filter(coniferspecies__coniferproduct__id__in=id_list_no_genus).distinct()
        
        fields['height_from'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .aggregate(min=Min('height_from'), max=Max('height_from'))
        
        fields['width_from'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .aggregate(min=Min('width_from'), max=Max('width_from'))

        fields['container'] = PlantPriceContainer.objects\
            .filter(coniferproductprice__product_id__in=id_list).distinct()

        fields['rs'] = PlantPriceRootSystem.objects\
            .filter(coniferproductprice__product_id__in=id_list).distinct()

        fields['shtamb'] = ConiferProductPrice.objects.filter(product_id__in=id_list).exclude(shtamb='')\
            .order_by('shtamb').distinct('shtamb').values_list('shtamb', flat=True)
        
        fields['extra'] = ConiferProductPrice.objects.filter(product_id__in=id_list)\
            .order_by('extra').distinct('extra').values_list('extra', flat=True)
        
        # from django.db import connection, connections
        # print(len(connection.queries))
        # print(sum(len(c.queries) for c in connections.all()))
        # for query in connections['default'].queries:
        #     print(query['time'])

        data = {}
        data.update({'genus': list(fields['genus'].values_list('id', flat=True))})
        data.update({'height_from': fields['height_from']})
        data.update({'width_from': fields['width_from']})
        data.update({'container': list(fields['container'].values_list('id', flat=True))})
        data.update({'rs': list(fields['rs'].values_list('id', flat=True))})
        data.update({'shtamb': [] if fields['shtamb'] else None})
        data.update({'extra': [] if True in fields['extra'] else None})

        return JsonResponse(data)
    
    return JsonResponse({})
