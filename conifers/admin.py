from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import PriceContainerFilter
from common.helpers import get_price_properties
from conifers.filters import ConiferProductGenusFilter, ConiferProductPriceGenusFilter
from conifers.forms import ConiferSpeciesAdminForm, ConiferProductAdminForm
from conifers.models import (
    ConiferSpecies, ConiferProduct, ConiferProductPrice)
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin


@admin.register(ConiferSpecies)
class ConiferSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = ConiferSpeciesAdminForm


class ConiferProductPriceInline(ProductPriceInline):
    model = ConiferProductPrice
    fields = ('container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )


@admin.register(ConiferProduct)
class ConiferProductAdmin(ProductAbstractAdmin):
    form = ConiferProductAdminForm
    list_filter = (ConiferProductGenusFilter, )
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


@admin.register(ConiferProductPrice)
class ConiferProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')
    
    list_filter = (ConiferProductPriceGenusFilter, PriceContainerFilter,)
    fields = ('product', 'container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
