from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin, RecommendedDetailMixin
from deciduous.models import DecProduct, DecSpecies
from pure_pagination.mixins import PaginationMixin


class DecProductList(PaginationMixin, PerPageMixin, PlantSpeciesFilterMixin,
                         PlantGenusFilterMixin, ListView):
    model = DecProduct
    template_name = 'deciduous/list.html'
    queryset = DecProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('prices')
    division_name = 'DEC'
    species_model = DecSpecies


class DecProductDetail(RecommendedDetailMixin, DetailView):
    model = DecProduct
    template_name = 'deciduous/detail.html'
    queryset = DecProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('planting') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container') \
        .prefetch_related('prices__rs')

