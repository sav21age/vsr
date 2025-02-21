from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, 
    ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from deciduous.models import DecProductPrice
from plants.models import PlantPriceContainer


class DecSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'DEC'


class DecProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'DEC'


class DecProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'DEC'


class DecProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = DecProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]
