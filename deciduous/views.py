from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.db.models import Min, Max, Prefetch
from common.mixins import PerPageMixin, RecommendedDetailMixin
from deciduous.forms import DecProductPriceFilterForm
from deciduous.mixins import DecFilterFormMixin
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from images.models import Image
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem
from pure_pagination.mixins import PaginationMixin
from videos.models import Video


class DecProductDetail(RecommendedDetailMixin, DetailView):
    model = DecProduct
    template_name = 'deciduous/detail.html'
    queryset = DecProduct.is_visible_objects.all() \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related(Prefetch('videos', queryset=Video.is_visible_objects.all())) \
        .prefetch_related('planting') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container') \
        .prefetch_related('prices__rs')


class DecProductList(PaginationMixin, 
                     DecFilterFormMixin,
                     PerPageMixin, 
                    #  PlantSpeciesFilterMixin, PlantGenusFilterMixin, 
                     ListView):
    model = DecProduct
    template_name = 'deciduous/list.html'
    queryset = DecProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related('prices')
    division_name = 'DEC'
    species_model = DecSpecies


def filter_form(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    form = DecProductPriceFilterForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data

        qs = DecProduct.is_visible_objects.all()\
            .prefetch_related('prices') \
            .prefetch_related('prices__container') \
            .prefetch_related('prices__rs')\
            # .prefetch_related('images') \
        # .prefetch_related('advantages')

        if clean['height_from']:
            qs = qs.filter(prices__height_from__gte=clean['height_from'])

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
            .filter(decspecies__decproduct__id__in=id_list_no_genus).distinct()

        fields['height_from'] = DecProductPrice.objects.filter(product_id__in=id_list)\
            .aggregate(min=Min('height_from'), max=Max('height_from'))

        fields['container'] = PlantPriceContainer.objects\
            .filter(decproductprice__product_id__in=id_list).distinct()

        fields['rs'] = PlantPriceRootSystem.objects\
            .filter(decproductprice__product_id__in=id_list).distinct()

        fields['shtamb'] = DecProductPrice.objects.filter(product_id__in=id_list).exclude(shtamb='')\
            .order_by('shtamb').distinct('shtamb').values_list('shtamb', flat=True)

        fields['extra'] = DecProductPrice.objects.filter(product_id__in=id_list)\
            .order_by('extra').distinct('extra').values_list('extra', flat=True)

        data = {}
        data.update({'genus': list(fields['genus'].values_list('id', flat=True))})
        data.update({'height_from': fields['height_from']})
        data.update({'container': list(fields['container'].values_list('id', flat=True))})
        data.update({'rs': list(fields['rs'].values_list('id', flat=True))})
        data.update({'shtamb': [] if fields['shtamb'] else None})
        data.update({'extra': [] if True in fields['extra'] else None})

        return JsonResponse(data)

    return JsonResponse({})
