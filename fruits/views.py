from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from common.mixins import PerPageMixin, RecommendedDetailMixin
from fruits.forms import FruitProductPriceFilterForm
from fruits.models import FruitProduct, FruitProductPriceAge, FruitSpecies
from images.models import Image
from plants.models import PlantGenus, PlantPriceContainer, PlantPriceRootSystem
from pure_pagination.mixins import PaginationMixin
from videos.models import Video


class FruitProductDetail(RecommendedDetailMixin, DetailView):
    model = FruitProduct
    template_name = 'fruits/detail.html'
    queryset = FruitProduct.is_visible_objects.all() \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related(Prefetch('videos', queryset=Video.is_visible_objects.all())) \
        .prefetch_related('advantages') \
        .prefetch_related(
            'prices',
            'prices__container',
            'prices__rs',
            'prices__age',
            'prices__rootstock'
    )


class FruitFilterFormMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        form = FruitProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data

            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                qs = qs.filter(species__genus__in=id_list)

            if clean['container']:
                qs = qs.filter(prices__container=clean['container'])

            if clean['rs']:
                qs = qs.filter(prices__rs=clean['rs'])

            if clean['age']:
                qs = qs.filter(prices__age=clean['age'])

            return qs.distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = FruitProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = FruitProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],
                    'container': clean['container'],
                    'rs': clean['rs'],
                    'age': clean['age'],

                    'per_page': clean['per_page'],
                },
            )
        else:
            context['form'] = FruitProductPriceFilterForm()
        return context


class FruitProductList(PaginationMixin, PerPageMixin,
                       FruitFilterFormMixin,
                    #    PlantSpeciesFilterMixin, PlantGenusFilterMixin,
                       ListView):
    model = FruitProduct
    template_name = 'fruits/list.html'
    queryset = FruitProduct.is_visible_objects.all()\
        .select_related('species') \
        .prefetch_related(Prefetch('images', queryset=Image.is_visible_objects.all())) \
        .prefetch_related('prices')
    division_name = 'FRU'
    species_model = FruitSpecies


def filter_form(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    form = FruitProductPriceFilterForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data

        qs = FruitProduct.is_visible_objects.all()\
            .prefetch_related('prices') \
            .prefetch_related('prices__container') \
            .prefetch_related('prices__rs')\
            # .prefetch_related('images') \
        # .prefetch_related('advantages')

        if clean['container']:
            qs = qs.filter(
                prices__container=clean['container'])

        if clean['rs']:
            qs = qs.filter(prices__rs=clean['rs'])

        if clean['age']:
            qs = qs.filter(prices__age=clean['age'])

        qs_no_genus = qs.distinct()
        id_list_no_genus = list(qs_no_genus.values_list('id', flat=True))

        if clean['genus']:
            id_list = list(clean['genus'].values_list('id', flat=True))
            qs = qs.filter(species__genus__in=id_list)

        qs = qs.distinct()
        id_list = list(qs.values_list('id', flat=True))

        fields = {}

        fields['genus'] = PlantGenus.objects\
            .filter(fruitspecies__fruitproduct__id__in=id_list_no_genus).distinct()

        fields['container'] = PlantPriceContainer.objects\
            .filter(fruitproductprice__product_id__in=id_list).distinct()

        fields['rs'] = PlantPriceRootSystem.objects\
            .filter(fruitproductprice__product_id__in=id_list).distinct()

        fields['age'] = FruitProductPriceAge.objects\
            .filter(fruitproductprice__product_id__in=id_list).distinct()

        data = {}
        data.update(
            {'genus': list(fields['genus'].values_list('id', flat=True))})
        data.update(
            {'container': list(fields['container'].values_list('id', flat=True))})
        data.update({'rs': list(fields['rs'].values_list('id', flat=True))})
        data.update({'age': list(fields['age'].values_list('id', flat=True))})

        return JsonResponse(data)

    return JsonResponse({})
