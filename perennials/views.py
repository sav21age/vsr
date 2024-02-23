from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin
from perennials.models import PerProduct, PerSpecies
from pure_pagination.mixins import PaginationMixin


class PerProductList(PaginationMixin, PerPageMixin, PlantSpeciesFilterMixin,
                       PlantGenusFilterMixin, ListView):
    model = PerProduct
    template_name = 'perennials/list.html'
    queryset = PerProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('perproductprice_set')
    division_name = 'PER'
    species_model = PerSpecies


class PerProductDetail(DetailView):
    model = PerProduct
    template_name = 'perennials/detail.html'
    queryset = PerProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('advantages') \
        .prefetch_related('perproductprice_set') \
        .prefetch_related('perproductprice_set__container')
