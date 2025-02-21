from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from perennials.models import PerProductPrice
from plants.models import PlantPriceContainer


class PerSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'PER'


class PerProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'PER'


class PerProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'PER'


class PerProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = PerProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]
