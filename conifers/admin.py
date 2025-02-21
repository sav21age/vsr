from django.contrib import admin
from common.admin import (
    ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible)
from conifers.actions import coniferproduct_batch_copy_admin
from conifers.filters import (
    ConiferProductGenusAdminFilter, ConiferProductPriceContainerAdminFilter,
    ConiferProductPriceGenusAdminFilter, ConiferSpeciesGenusAdminFilter)
from conifers.forms import ConiferSpeciesAdminForm, ConiferProductAdminForm
from conifers.models import (
    ConiferSpecies, ConiferProduct, ConiferProductPrice)
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from videos.admin import VideoInline


@admin.register(ConiferSpecies)
class ConiferSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = ConiferSpeciesAdminForm
    list_display = ('name', 'genus', 'get_count')
    list_filter = (ConiferSpeciesGenusAdminFilter,)

    def get_count(self, obj=None):
        if obj:
            return ConiferProduct.objects.filter(species__name=obj.name).count()
        return ''
    get_count.short_description = 'количество'

    def has_delete_permission(self, request, obj=None):
        if obj:
            count = ConiferProduct.objects.filter(
                species__name=obj.name).count()
            if count > 0:
                return False
        return True


# --


class ConiferProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs')

    model = ConiferProductPrice
    fields = ('container', ('height_from', 'height_to'), ('width_from', 'width_to'),
              'rs', 'shtamb', 'extra', 'planting_year', 'price', 'updated_at',)


@admin.register(ConiferProduct)
class ConiferProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     return actions

    form = ConiferProductAdminForm
    list_filter = (ConiferProductGenusAdminFilter, )
    actions = (coniferproduct_batch_copy_admin, make_visible, make_hidden,)
    inlines = [ImageInline, VideoInline, ConiferProductPriceInline, ]
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
            'fields': ('name', 'name_trans_words', 'slug', 'scientific_name', 'short_description', 'needles',)
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


@admin.register(ConiferProductPrice)
class ConiferProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (ConiferProductPriceGenusAdminFilter,
                   ConiferProductPriceContainerAdminFilter,)
    fields = ('product', 'container',
              ('height_from', 'height_to'), ('width_from', 'width_to',),
              'rs', 'shtamb', 'extra', 'planting_year', 'price', )
    list_display = ('get_product', 'updated_at', 'price', )

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
