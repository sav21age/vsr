from django.contrib import admin

from common.admin import (ProductAbstractAdmin, ProductPriceAbstractAdmin,
                          ProductPriceInline, make_hidden, make_visible)
from fruits.actions import fruitproduct_batch_copy_admin
from fruits.filters import (FruitProductGenusAdminFilter,
                            FruitProductPriceAgeAdminFilter,
                            FruitProductPriceContainerAdminFilter,
                            FruitProductPriceGenusAdminFilter,
                            FruitProductPriceRootStockAdminFilter,
                            FruitSpeciesGenusAdminFilter)
from fruits.forms import FruitProductAdminForm, FruitSpeciesAdminForm
from fruits.models import (FruitProduct, FruitProductPrice,
                           FruitProductPriceAge, FruitProductPriceRootstock,
                           FruitSpecies)
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from videos.admin import VideoInline


@admin.register(FruitSpecies)
class FruitSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = FruitSpeciesAdminForm
    list_display = ('name', 'genus', 'get_count')
    list_filter = (FruitSpeciesGenusAdminFilter,)

    def get_count(self, obj=None):
        if obj:
            return FruitProduct.objects.filter(species__name=obj.name).count()
        return ''
    get_count.short_description = 'количество'

    def has_delete_permission(self, request, obj=None):
        if obj:
            count = FruitProduct.objects.filter(species__name=obj.name).count()
            if count > 0:
                return False
        return True


# --

admin.site.register(FruitProductPriceAge)

admin.site.register(FruitProductPriceRootstock)

# --

class FruitProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs', 'age')

    model = FruitProductPrice
    fields = ('container', ('height_from', 'height_to'), ('width_from', 'width_to',),
              'rs', 'age', 'rootstock', 'price', 'updated_at', )


@admin.register(FruitProduct)
class FruitProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    form = FruitProductAdminForm
    list_filter = (FruitProductGenusAdminFilter, )
    actions = (fruitproduct_batch_copy_admin, make_visible, make_hidden,)
    inlines = [ImageInline, VideoInline, FruitProductPriceInline, ]
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
            'fields': ('name', 'name_trans_words', 'slug', 'scientific_name', 'short_description',)
        }),
        ('Размеры', {
            'fields': ('height', 'width', )
        }),
        ('', {
            'fields': ('flowering', 'self_fertility', )
        }),
        ('Плоды', {
            'classes': ('collapse',),
            'fields': ('fruit_ripening', ('fruit_dimension', 'fruit_size', 'fruit_weight', ), 'fruit_taste', 'fruit_keeping_quality', 'beginning_fruiting', )
        }),
        ('', {
            'fields': ('advantages', 'features', 'description', )
        }),
    )


# --


@admin.register(FruitProductPrice)
class FruitProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs') \
            .select_related('age') \
            .select_related('rootstock')

    list_filter = (FruitProductPriceGenusAdminFilter,
                   FruitProductPriceAgeAdminFilter,
                   FruitProductPriceContainerAdminFilter, 
                   FruitProductPriceRootStockAdminFilter,)
    
    fields = ('product', 'container', 
              ('height_from', 'height_to'), ('width_from', 'width_to',),
              'rs', 'age', 'rootstock', 'price', )
    
    list_display = ('get_product', 'updated_at', 'price', )
    # show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
