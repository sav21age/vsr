from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin, RecommendedDetailMixin
from conifers.models import ConiferProduct, ConiferSpecies
from pure_pagination.mixins import PaginationMixin


class ConiferProductList(PaginationMixin, PerPageMixin, PlantSpeciesFilterMixin, 
                         PlantGenusFilterMixin, ListView):
    model = ConiferProduct
    template_name = 'conifers/list.html'
    queryset = ConiferProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('coniferproductprice_set')
    division_name = 'CON'
    species_model = ConiferSpecies


class ConiferProductDetail(RecommendedDetailMixin, DetailView):
    model = ConiferProduct
    template_name = 'conifers/detail.html'
    queryset = ConiferProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('advantages') \
        .prefetch_related('coniferproductprice_set') \
        .prefetch_related('coniferproductprice_set__container')
