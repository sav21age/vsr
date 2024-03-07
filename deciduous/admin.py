from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter)
from common.helpers import get_price_properties
from deciduous.forms import DecProductAdminForm, DecSpeciesAdminForm
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


@admin.register(DecSpecies)
class DecSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = DecSpeciesAdminForm


class DecProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs')

    model = DecProductPrice
    fields = ('container', 'height', 'width', 'trunk_diameter',
              'rs', 'shtamb', 'extra', 'price', )


#--


class DecProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'DEC'


@admin.register(DecProduct)
class DecProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('decproductprice_set')

    save_as = True
    form = DecProductAdminForm
    list_filter = (DecProductGenusAdminFilter, )
    inlines = [DecProductPriceInline, ImageInline, ]
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
            'fields': ('name', 'slug', 'scientific_name', 'short_description', 'leaves')
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('Цветение', {
            'classes': ('collapse',),
            'fields': ('flowering',  'flowering_period', 'flower_size', 'inflorescence', 'inflorescence_size', )
        }),
        ('', {
            'fields': ('planting', 'shelter_winter', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description',)
        }),
    )


#--


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


@admin.register(DecProductPrice)
class DecProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (DecProductPriceGenusAdminFilter, DecProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
