from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from common.mixins import PerPageMixin, RecommendedDetailMixin
from images.models import Image
from pure_pagination.mixins import PaginationMixin
from roses.mixins import RoseSpeciesFilterMixin
from roses.models import RoseProduct, RoseSpecies
from videos.models import Video


class RoseProductList(PaginationMixin, PerPageMixin, RoseSpeciesFilterMixin, ListView):
    model = RoseProduct
    template_name = 'roses/list.html'
    queryset = RoseProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related('prices')
    species_model = RoseSpecies


class RoseProductDetail(RecommendedDetailMixin, DetailView):
    model = RoseProduct
    template_name = 'roses/detail.html'
    queryset = RoseProduct.is_visible_objects.all() \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related(Prefetch('videos', queryset=Video.is_visible_objects.all())) \
        .prefetch_related('advantages') \
        .prefetch_related('prices') \
        .prefetch_related('prices__container')

