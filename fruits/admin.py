from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter)
from common.helpers import get_price_properties
from fruits.forms import FruitProductAdminForm, FruitSpeciesAdminForm
from fruits.models import FruitProduct, FruitProductPrice, FruitProductPriceAge, FruitSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


@admin.register(FruitSpecies)
class FruitSpeciesAdmin(PlantSpeciesAbstractAdmin):
    form = FruitSpeciesAdminForm


class FruitProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs', 'age')

    model = FruitProductPrice
    fields = ('container', 'height', 'width',
              'rs', 'age', 'price', )


# --


class FruitProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'FRU'


@admin.register(FruitProduct)
class FruitProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('fruitproductprice_set')

    save_as = True
    form = FruitProductAdminForm
    list_filter = (FruitProductGenusAdminFilter, )
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


# --


class FruitProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'FRU'


class FruitProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = FruitProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)
        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')
        return [(o.id, o.name) for o in qs]


class FruitProductPriceAgeAdminFilter(SimpleListFilter):
    title = 'Возраст'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        qs = FruitProductPrice.objects.exclude(age_id__isnull=True)\
            .order_by('age_id')\
            .distinct('age_id')\
            .values_list('age_id', flat=True)

        lst = list(qs)
        qs = FruitProductPriceAge.objects.filter(id__in=lst)
        return [(o.id, o) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(age__id__exact=self.value())

        return queryset


@admin.register(FruitProductPrice)
class FruitProductPriceAdmin(ProductPriceAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('product') \
            .select_related('container') \
            .select_related('rs')

    list_filter = (FruitProductPriceGenusAdminFilter,
                   FruitProductPriceAgeAdminFilter, 
                   FruitProductPriceContainerAdminFilter, )
    fields = ('product', 'container', 'height', 'width',
              'rs', 'age', 'price', )
    list_display = ('get_product', 'price', )
    # show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            return f"{obj.product} {get_price_properties(obj)}"
        return ''
    get_product.short_description = 'растение'
