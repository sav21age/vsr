from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import PriceContainerFilter
from common.helpers import get_price_properties
from images.admin import ImageInline
from roses.forms import RoseProductAdminForm, RoseSpeciesAdminForm
from roses.models import RoseProduct, RoseProductPrice, RoseSpecies


@admin.register(RoseSpecies)
class RoseSpeciesAdmin(admin.ModelAdmin):
    form = RoseSpeciesAdminForm


class RoseProductPriceInline(ProductPriceInline):
    model = RoseProductPrice
    fields = ('container', 'price', )


@admin.register(RoseProduct)
class RoseProductAdmin(ProductAbstractAdmin):
    form = RoseProductAdminForm
    list_filter = ('species', )
    inlines = [RoseProductPriceInline, ImageInline, ]
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
            'fields': ('name', 'slug', 'scientific_name', 'short_description', )
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        # ('', {
        #     'fields': ('flowering_period', 'flowering', 'flower_size', 'inflorescence_size', 'inflorescence_description',)
        # }),
        ('', {
            'fields': ('flowering', 'flavor', 'flower_size', 'quantity_on_stem', 'resistance_fungus', 'resistance_rain', 'shelter_winter', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description',)
        }),
    )


@admin.register(RoseProductPrice)
class RoseProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (PriceContainerFilter,)
    fields = ('product', 'container', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
