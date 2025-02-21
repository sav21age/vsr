from django.contrib import admin

from common.admin import (ProductAbstractAdmin, ProductPriceAbstractAdmin,
                          ProductPriceInline, make_hidden, make_visible)
from images.admin import ImageInline
from roses.actions import roseproduct_batch_copy_admin
from roses.filters import RoseProductPriceContainerAdminFilter
from roses.forms import (RoseProductAdminForm, RoseSpeciesAdminForm)
from roses.models import RoseProduct, RoseProductPrice, RoseSpecies
from videos.admin import VideoInline


@admin.register(RoseSpecies)
class RoseSpeciesAdmin(admin.ModelAdmin):
    form = RoseSpeciesAdminForm


# --


class RoseProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container')

    model = RoseProductPrice
    fields = ('container', 'price', 'updated_at', )


@admin.register(RoseProduct)
class RoseProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')
        # .prefetch_related('roseproductprice_set')

    form = RoseProductAdminForm
    show_facets = admin.ShowFacets.ALWAYS
    list_filter = ('species', )
    actions = (roseproduct_batch_copy_admin, make_visible, make_hidden,)
    inlines = [ImageInline, VideoInline,  RoseProductPriceInline,]
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
            'fields': ('name', 'name_trans_words', 'slug', 'scientific_name', 'short_description', )
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('', {
            'fields': ('flowering', 'flavor', 'flower_size', 'quantity_on_stem', 'resistance_fungus', 'resistance_rain', )
        }),
        ('', {
            'fields': ('shelter_winter', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'description',)
        }),
    )


# --


@admin.register(RoseProductPrice)
class RoseProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (RoseProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'price', )
    list_display = ('get_product', 'updated_at', 'price', )
    show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
