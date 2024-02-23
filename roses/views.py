from django.views.generic import ListView, DetailView
from common.mixins import PerPageMixin
from pure_pagination.mixins import PaginationMixin
from roses.mixins import RoseSpeciesFilterMixin
from roses.models import RoseProduct, RoseSpecies


class RoseProductList(PaginationMixin, PerPageMixin, RoseSpeciesFilterMixin, ListView):
    model = RoseProduct
    template_name = 'roses/list.html'
    queryset = RoseProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('roseproductprice_set')
    species_model = RoseSpecies


class RoseProductDetail(DetailView):
    model = RoseProduct
    template_name = 'roses/detail.html'
    queryset = RoseProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('advantages') \
        .prefetch_related('roseproductprice_set') \
        .prefetch_related('roseproductprice_set__container')


