from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin
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


class DecProductDetail(DetailView):
    model = DecProduct
    template_name = 'deciduous/detail.html'
    queryset = DecProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('planting') \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container') \
        .prefetch_related('prices__rs')

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
