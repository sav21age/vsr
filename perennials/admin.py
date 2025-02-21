from django.contrib import admin

from common.admin import (ProductAbstractAdmin, ProductPriceAbstractAdmin,
                          ProductPriceInline, make_hidden, make_visible)
from images.admin import ImageInline
from perennials.actions import perproduct_batch_copy_admin
from perennials.filters import (PerProductGenusAdminFilter,
                                PerProductPriceContainerAdminFilter,
                                PerProductPriceGenusAdminFilter,
                                PerSpeciesGenusAdminFilter)
from perennials.forms import (PerProductAdminForm,
                              PerSpeciesAdminForm)
from perennials.models import (PerProduct, PerProductFlowering,
                               PerProductPrice, PerSpecies)
from plants.admin import PlantSpeciesAbstractAdmin
from videos.admin import VideoInline


@admin.register(PerSpecies)
class PerSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = PerSpeciesAdminForm
    list_display = ('name', 'genus', 'get_count')
    list_filter = (PerSpeciesGenusAdminFilter,)

    def get_count(self, obj=None):
        if obj:
            return PerProduct.objects.filter(species__name=obj.name).count()
        return ''
    get_count.short_description = 'количество'

    def has_delete_permission(self, request, obj=None):
        if obj:
            count = PerProduct.objects.filter(species__name=obj.name).count()
            if count > 0:
                return False
        return True


# --

admin.site.register(PerProductFlowering)

# --


class PerProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container')

    model = PerProductPrice
    fields = ('container', 'planting_year', 'price', 'updated_at', )


@admin.register(PerProduct)
class PerProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    form = PerProductAdminForm
    list_filter = (PerProductGenusAdminFilter, )
    actions = (perproduct_batch_copy_admin, make_visible, make_hidden,)
    inlines = [ImageInline, VideoInline, PerProductPriceInline, ]
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
            'fields': ('name', 'name_trans_words', 'slug', 'scientific_name', 'short_description', 'leaves', )
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('Цветение', {
            'classes': ('collapse',),
            'fields': ('flowering', 'flowering_duration', 'flowering_period', 'flower_size', 'inflorescence_size',)
        }),
        ('', {
            'fields': ('planting', 'shelter_winter', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description', )
        }),
    )


# --


@admin.register(PerProductPrice)
class PerProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (PerProductPriceGenusAdminFilter,
                   PerProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'planting_year', 'price', )
    list_display = ('get_product', 'updated_at', 'price', )

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
