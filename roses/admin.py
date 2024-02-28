from django.contrib import admin
from django.contrib.admin import SimpleListFilter
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


class RosePriceContainerFilter(SimpleListFilter):
    title = 'Контейнер'
    parameter_name = 'container'
    container = ''

    def lookups(self, request, model_admin):
        qs = RoseProductPrice.objects.select_related('container')\
            .only('container__id', 'container__name')\
            .order_by('container__id')\
            .distinct('container__id')
        return [(o.container.id, o.container.name) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(container__id__exact=self.value())

        return queryset
    

@admin.register(RoseProductPrice)
class RoseProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container')

    list_filter = (RosePriceContainerFilter,)
    fields = ('product', 'container', 'price', )
    list_display = ('get_product', 'price', )
    show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
