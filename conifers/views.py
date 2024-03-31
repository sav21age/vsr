from django.views.generic import ListView, DetailView
from common.mixins import PlantGenusFilterMixin, PerPageMixin, PlantSpeciesFilterMixin
from conifers.models import ConiferProduct, ConiferSpecies
from pure_pagination.mixins import PaginationMixin


class ConiferProductList(PaginationMixin, PerPageMixin, PlantSpeciesFilterMixin, 
                         PlantGenusFilterMixin, ListView):
    model = ConiferProduct
    template_name = 'conifers/list.html'
    queryset = ConiferProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related('images') \
        .prefetch_related('prices')
    division_name = 'CON'
    species_model = ConiferSpecies


class ConiferProductDetail(DetailView):
    model = ConiferProduct
    template_name = 'conifers/detail.html'
    queryset = ConiferProduct.is_visible_objects.all() \
        .prefetch_related('images') \
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
