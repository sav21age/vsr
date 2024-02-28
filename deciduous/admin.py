from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import PriceContainerFilter
from common.helpers import get_price_properties
from deciduous.filters import DecProductGenusFilter, DecProductPriceGenusFilter
from deciduous.forms import DecProductAdminForm, DecSpeciesAdminForm
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin


@admin.register(DecSpecies)
class DecSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = DecSpeciesAdminForm


class DecProductPriceInline(ProductPriceInline):
    model = DecProductPrice
    fields = ('container', 'height', 'width', 'trunk_diameter',
              'rs', 'shtamb', 'extra', 'price', )
   

@admin.register(DecProduct)
class DecProductAdmin(ProductAbstractAdmin):
    form = DecProductAdminForm
    list_filter = (DecProductGenusFilter, )
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
            'fields': ('planting', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description',)
        }),
    )

@admin.register(DecProductPrice)
class DecProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (DecProductPriceGenusFilter, PriceContainerFilter,)
    fields = ('product', 'container', 'height', 'width',
              'rs', 'shtamb', 'extra', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
