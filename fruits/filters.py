from django.contrib.admin import SimpleListFilter

from common.filters import (ProductGenusAdminFilter,
                            ProductPriceContainerAdminFilter,
                            ProductPriceGenusAdminFilter,
                            SpeciesGenusAdminFilter)
from fruits.models import FruitProductPrice, FruitProductPriceAge
from plants.models import PlantPriceContainer, PlantPriceRootSystem


class FruitSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'FRU'


class FruitProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'FRU'


class FruitProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'FRU'


class FruitProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = FruitProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)
        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')
        return [(o.id, o.name) for o in qs]


class FruitProductPriceAgeAdminFilter(SimpleListFilter):
    title = 'Возраст'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        qs = FruitProductPrice.objects.exclude(age_id__isnull=True)\
            .order_by('age_id')\
            .distinct('age_id')\
            .values_list('age_id', flat=True)

        lst = list(qs)
        qs = FruitProductPriceAge.objects.filter(id__in=lst)
        return [(o.id, o) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(age__id__exact=self.value())

        return queryset


class FruitProductPriceRootStockAdminFilter(SimpleListFilter):
    title = 'Корневая система'
    parameter_name = 'rs'

    def lookups(self, request, model_admin):
        qs = FruitProductPrice.objects.exclude(rs_id__isnull=True)\
            .order_by('rs_id')\
            .distinct('rs_id')\
            .values_list('rs_id', flat=True)

        lst = list(qs)
        qs = PlantPriceRootSystem.objects.filter(id__in=lst)
        return [(o.id, o) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rs__id__exact=self.value())

        return queryset
