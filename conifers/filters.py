from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, 
    ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from conifers.models import ConiferProductPrice
from plants.models import PlantPriceContainer


class ConiferSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'CON'


class ConiferProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'CON'


class ConiferProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'CON'


class ConiferProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        # qs = ConiferProductPrice.objects.exclude(container__isnull=True)\
        #     .select_related('container')\
        #     .only('container__id', 'container__name')\
        #     .order_by('container__id')\
        #     .distinct('container__id')
        # return [(o.container.id, o.container.name) for o in qs]
        qs = ConiferProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]
