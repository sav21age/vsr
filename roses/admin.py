from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import ProductPriceContainerAdminFilter
from common.helpers import get_price_properties
from images.admin import ImageInline
from plants.models import PlantPriceContainer
from roses.forms import RoseProductAdminForm, RoseSpeciesAdminForm
from roses.models import RoseProduct, RoseProductPrice, RoseSpecies


@admin.register(RoseSpecies)
class RoseSpeciesAdmin(admin.ModelAdmin):
    form = RoseSpeciesAdminForm


class RoseProductPriceInline(ProductPriceInline):
    model = RoseProductPrice
    fields = ('container', 'price', )


# --


@admin.register(RoseProduct)
class RoseProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('roseproductprice_set')

    form = RoseProductAdminForm
    show_facets = admin.ShowFacets.ALWAYS
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
        ('', {
            'fields': ('flowering', 'flavor', 'flower_size', 'quantity_on_stem', 'resistance_fungus', 'resistance_rain', 'shelter_winter', 'winter_zone', )
        }),
        ('', {
            'fields': ('advantages', 'description',)
        }),
    )


# --


class RoseProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = RoseProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]


@admin.register(RoseProductPrice)
class RoseProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (RoseProductPriceContainerAdminFilter,)
    fields = ('product', 'container', 'price', )
    list_display = ('get_product', 'price', )
    show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
