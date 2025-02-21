from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from deciduous.actions import decproduct_batch_copy_admin
from deciduous.filters import (
    DecProductGenusAdminFilter, DecProductPriceContainerAdminFilter, 
    DecProductPriceGenusAdminFilter, DecSpeciesGenusAdminFilter)
from deciduous.forms import DecProductAdminForm, DecSpeciesAdminForm
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from videos.admin import VideoInline


@admin.register(DecSpecies)
class DecSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = DecSpeciesAdminForm
    list_display = ('name', 'genus', 'get_count')
    list_filter = (DecSpeciesGenusAdminFilter,)

    def get_count(self, obj=None):
        if obj:
            return DecProduct.objects.filter(species__name=obj.name).count()
        return ''
    get_count.short_description = 'количество'

    def has_delete_permission(self, request, obj=None):
        if obj:
            count = DecProduct.objects.filter(species__name=obj.name).count()
            if count > 0:
                return False
        return True


# --


class DecProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs')

    model = DecProductPrice
    fields = ('container', ('height_from', 'height_to'), ('width_from', 'width_to'), 'trunk_diameter',
              'rs', 'shtamb', 'extra', 'bush', 'planting_year', 'price', 'updated_at', )


@admin.register(DecProduct)
class DecProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    form = DecProductAdminForm
    list_filter = (DecProductGenusAdminFilter, )
    actions = (decproduct_batch_copy_admin, make_visible, make_hidden,)
    inlines = [ImageInline, VideoInline, DecProductPriceInline, ]
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
            'fields': ('name', 'name_trans_words', 'slug', 'scientific_name', 'short_description', 'leaves', 'crown')
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


# --


@admin.register(DecProductPrice)
class DecProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (DecProductPriceGenusAdminFilter,
                   DecProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 
              ('height_from', 'height_to'), ('width_from', 'width_to'),
              'rs', 'shtamb', 'extra', 'bush', 'planting_year', 'price',)
    list_display = ('get_product', 'updated_at', 'price', )

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
