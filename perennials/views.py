from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.db.models.functions import Cast
from django.db.models import IntegerField, Prefetch
from common.mixins import PerPageMixin, RecommendedDetailMixin
from images.models import Image
from perennials.forms import PerProductPriceFilterForm
from perennials.mixins import PerFilterFormMixin
from perennials.models import PerProduct, PerProductPrice, PerSpecies
from plants.models import PlantGenus, PlantPriceContainer
from pure_pagination.mixins import PaginationMixin
from videos.models import Video


class PerProductDetail(RecommendedDetailMixin, DetailView):
    model = PerProduct
    template_name = 'perennials/detail.html'
    queryset = PerProduct.is_visible_objects.all() \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related(Prefetch('videos', queryset=Video.is_visible_objects.all())) \
        .prefetch_related('flowering') \
        .prefetch_related('planting') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container')



    

class PerProductList(PaginationMixin, PerPageMixin, 
                     PerFilterFormMixin,
                    #  PlantSpeciesFilterMixin, PlantGenusFilterMixin, 
                     ListView):
    model = PerProduct
    template_name = 'perennials/list.html'
    queryset = PerProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related('prices')
    division_name = 'PER'
    species_model = PerSpecies


def filter_form(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    form = PerProductPriceFilterForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data

        qs = PerProduct.is_visible_objects.all()\
            .prefetch_related('prices') \
            .prefetch_related('prices__container') \
            .prefetch_related('prices__rs')\

        if clean['container']:
            qs = qs.filter(prices__container=clean['container'])

        if clean['planting_year']:
            qs = qs.filter(prices__planting_year=clean['planting_year'])

        qs_no_genus = qs.distinct()
        id_list_no_genus = list(qs_no_genus.values_list('id', flat=True))

        if clean['genus']:
            id_list = list(clean['genus'].values_list('id', flat=True))
            qs = qs.filter(species__genus__in=id_list)

        qs = qs.distinct()
        id_list = list(qs.values_list('id', flat=True))

        fields = {}

        fields['genus'] = PlantGenus.objects\
            .filter(perspecies__perproduct__id__in=id_list_no_genus).distinct()

        fields['container'] = PlantPriceContainer.objects\
            .filter(perproductprice__product_id__in=id_list).distinct()

        # fields['planting_year'] = PerProductPrice.objects.exclude(planting_year='').values_list(
        #     'planting_year', flat=True).order_by('planting_year').distinct('planting_year')

        fields['planting_year'] = PerProductPrice.objects.annotate(planting_year_integer=Cast('planting_year', output_field=IntegerField()))\
            .filter(product_id__in=id_list)\
            .exclude(planting_year='') \
            .order_by('planting_year').distinct('planting_year').values_list('planting_year_integer', flat=True)
        
        data = {}
        data.update(
            {'genus': list(fields['genus'].values_list('id', flat=True))})
        data.update(
            {'container': list(fields['container'].values_list('id', flat=True))})
        data.update({'planting_year': list(fields['planting_year'])})
        return JsonResponse(data)

    return JsonResponse({})
