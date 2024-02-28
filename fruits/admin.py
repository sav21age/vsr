from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import PriceContainerFilter
from common.helpers import get_price_properties
from fruits.filters import FruitProductGenusFilter, FruitProductPriceGenusFilter
from fruits.forms import FruitProductAdminForm, FruitSpeciesAdminForm
from fruits.models import FruitProduct, FruitProductPrice, FruitSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin


@admin.register(FruitSpecies)
class FruitSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = FruitSpeciesAdminForm


class FruitProductPriceInline(ProductPriceInline):
    model = FruitProductPrice
    fields = ('container', 'height', 'width',
              'rs', 'age', 'price', )


# admin.site.register(FruitProductPriceAge)


@admin.register(FruitProduct)
class FruitProductAdmin(ProductAbstractAdmin):
    form = FruitProductAdminForm
    list_filter = (FruitProductGenusFilter, )
    inlines = [FruitProductPriceInline, ImageInline, ]
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
            'fields': ('name', 'slug', 'scientific_name', 'short_description',)
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('', {
            'fields': ('flowering', 'rootstock', )
        }),
        ('Плоды', {
            'classes': ('collapse',),
            'fields': ('fruit_ripening', 'fruit_size', 'fruit_taste', 'fruit_keeping_quality', 'beginning_fruiting', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description', )
        }),
    )


@admin.register(FruitProductPrice)
class FruitProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (FruitProductPriceGenusFilter, 'age', PriceContainerFilter,)
    fields = ('product', 'container', 'height', 'width',
              'rs', 'age', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
