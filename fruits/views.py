from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin
from fruits.models import FruitProduct, FruitSpecies
from pure_pagination.mixins import PaginationMixin


class FruitProductList(PaginationMixin, PerPageMixin, PlantSpeciesFilterMixin,
                     PlantGenusFilterMixin, ListView):
    model = FruitProduct
    template_name = 'fruits/list.html'
    queryset = FruitProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('prices')
    division_name = 'FRU'
    species_model = FruitSpecies


class FruitProductDetail(DetailView):
    model = FruitProduct
    template_name = 'fruits/detail.html'
    queryset = FruitProduct.is_visible_objects.all() \
        .prefetch_related('images') \
        .prefetch_related('advantages') \
        .prefetch_related(
            'prices',
            'prices__container',
            'prices__rs',
            'prices__age',
            'prices__rootstock'
        )

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
