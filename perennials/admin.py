from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter)
from common.helpers import get_price_properties
from images.admin import ImageInline
from perennials.forms import PerProductAdminForm, PerSpeciesAdminForm
from perennials.models import PerProduct, PerProductPrice, PerSpecies
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


@admin.register(PerSpecies)
class PerSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = PerSpeciesAdminForm


class PerProductPriceInline(ProductPriceInline):
    model = PerProductPrice
    fields = ('container', 'price', )


# --


class PerProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'PER'


@admin.register(PerProduct)
class PerProductAdmin(ProductAbstractAdmin):
    form = PerProductAdminForm
    list_filter = (PerProductGenusAdminFilter, )
    inlines = [PerProductPriceInline, ImageInline, ]
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
            'fields': ('name', 'slug', 'scientific_name', 'short_description', 'leaves', )
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('Цветение', {
            'classes': ('collapse',),
            'fields': ('flowering', 'flowering_duration', 'flowering_period', 'flower_size', 'inflorescence_size',)
        }),
        ('', {
            'fields': ('planting', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description', )
        }),
    )


# --


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


@admin.register(PerProductPrice)
class PerProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (PerProductPriceGenusAdminFilter,
                   PerProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
