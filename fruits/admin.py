from django.contrib import admin
from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.admin import SimpleListFilter
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from fruits.forms import FruitProductAdminForm, FruitProductBatchCopyAdminForm, FruitSpeciesAdminForm
from fruits.models import FruitProduct, FruitProductPrice, FruitProductPriceAge, FruitProductPriceRootstock, FruitSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


class FruitSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'FRU'


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


class FruitProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container', 'rs', 'age')

    model = FruitProductPrice
    fields = ('container', 'height', 'width',
              'rs', 'age', 'rootstock', 'price', )


# --


admin.site.register(FruitProductPriceAge)
admin.site.register(FruitProductPriceRootstock)


# --


def batch_copy(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = FruitProductBatchCopyAdminForm(request.POST)

        if form.is_valid():
            clean = form.cleaned_data
            donor = form.cleaned_data['object_donor']
            for recipient in queryset:
                try:
                    with transaction.atomic():
                        if clean['scientific_name_chk']:
                            recipient.scientific_name = donor.scientific_name

                        if clean['height_chk']:
                            recipient.height = donor.height

                        if clean['width_chk']:
                            recipient.width = donor.width

                        if clean['advantages_chk']:
                            recipient.advantages.clear()
                            for attr in donor.advantages.all():
                                recipient.advantages.add(attr)

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['self_fertility_chk']:
                            recipient.self_fertility = donor.self_fertility

                        # if clean['rootstock_chk']:
                        #     recipient.rootstock = donor.rootstock

                        if clean['fruit_ripening_chk']:
                            recipient.fruit_ripening = donor.fruit_ripening

                        if clean['fruit_taste_chk']:
                            recipient.fruit_taste = donor.fruit_taste

                        if clean['fruit_dimension_chk']:
                            recipient.fruit_dimension = donor.fruit_dimension

                        if clean['fruit_size_chk']:
                            recipient.fruit_size = donor.fruit_size

                        if clean['fruit_weight_chk']:
                            recipient.fruit_weight = donor.fruit_weight

                        if clean['fruit_keeping_quality_chk']:
                            recipient.fruit_keeping_quality = donor.fruit_keeping_quality

                        if clean['beginning_fruiting_chk']:
                            recipient.beginning_fruiting = donor.beginning_fruiting

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = FruitProductBatchCopyAdminForm(request.POST)
    else:
        form = FruitProductBatchCopyAdminForm(initial={
            '_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})

    return render(
        request,
        'admin/batch_copy.html',
        {
            'object_recipients': queryset,
            'action': 'batch_copy',
            'form': form,
        }
    )


batch_copy.short_description = 'Пакетное копирование свойств'


class FruitProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'FRU'


@admin.register(FruitProduct)
class FruitProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    form = FruitProductAdminForm
    list_filter = (FruitProductGenusAdminFilter, )
    actions = (batch_copy, make_visible, make_hidden,)
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
            .select_related('rs') \
            .select_related('age') \
            .select_related('rootstock')

    list_filter = (FruitProductPriceGenusAdminFilter,
                   FruitProductPriceAgeAdminFilter,
                   FruitProductPriceContainerAdminFilter, )
    fields = ('product', 'container', 'height', 'width',
              'rs', 'age', 'rootstock', 'price', )
    list_display = ('get_product', 'price', )
    # show_facets = admin.ShowFacets.ALLOW

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
