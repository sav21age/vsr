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
        .prefetch_related('prices')
    division_name = 'PER'
    species_model = PerSpecies


class PerProductDetail(DetailView):
    model = PerProduct
    template_name = 'perennials/detail.html'
    queryset = PerProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('flowering') \
        .prefetch_related('planting') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context['object']
        context['recommended'] = self.model.is_visible_objects \
            .filter(species=obj.species) \
            .prefetch_related('images') \
            .prefetch_related('prices') \
            .exclude(id=obj.id)\
            .distinct()[:4]

        return context
