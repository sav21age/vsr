from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter)
from common.helpers import get_price_properties
from conifers.forms import ConiferSpeciesAdminForm, ConiferProductAdminForm
from conifers.models import (
    ConiferSpecies, ConiferProduct, ConiferProductPrice)
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


@admin.register(ConiferSpecies)
class ConiferSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = ConiferSpeciesAdminForm


class ConiferProductPriceInline(ProductPriceInline):
    model = ConiferProductPrice
    fields = ('container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )


# --


class ConiferProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'CON'


@admin.register(ConiferProduct)
class ConiferProductAdmin(ProductAbstractAdmin):
    form = ConiferProductAdminForm
    list_filter = (ConiferProductGenusAdminFilter, )
    inlines = [ConiferProductPriceInline, ImageInline, ]
    filter_horizontal = ('advantages', )
    fieldsets = (
        ('', {
            'fields': ('is_visible',)
        }),
        ('Промо', {
            'fields': ('head_title', 'meta_description',)
        }),
        ('Классификация растений', {
            'fields': ('species', )
        }),
        ('', {
            'fields': ('name', 'slug', 'scientific_name', 'short_description', 'needles',)
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('Дополнительные размеры', {
            'classes': ('collapse',),
            'fields': ('height10', 'width10', 'height1', 'width1', )
        }),
        ('', {
            'fields': ('planting', 'shelter', 'winter_zone', )
        }),        
        ('', {
            'fields': ('advantages', 'features', 'description', )
        }),
    )


# --


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


@admin.register(ConiferProductPrice)
class ConiferProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')
    
    list_filter = (ConiferProductPriceGenusAdminFilter, ConiferProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
