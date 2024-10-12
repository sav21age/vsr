from django.views.generic import ListView
from common.mixins import PerPageMixin, PlantDivisionFilterMixin
from pure_pagination.mixins import PaginationMixin
from seedlings.models import Seedling


class SeedlingList(PaginationMixin,
                        #  ConiferFilterFormMixin,
                         PerPageMixin,
                        #  PlantSpeciesFilterMixin, 
                        #  PlantGenusFilterMixin,
                         PlantDivisionFilterMixin,
                         ListView):
    model = Seedling
    template_name = 'seedlings/list.html'
    queryset = Seedling.is_visible_objects.all()