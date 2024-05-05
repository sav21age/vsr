from django.contrib import admin
from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from conifers.forms import ConiferProductBatchCopyAdminForm, ConiferSpeciesAdminForm, ConiferProductAdminForm
from conifers.models import (
    ConiferSpecies, ConiferProduct, ConiferProductPrice)
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


class ConiferSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'CON'


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
              'rs', 'shtamb', 'extra', 'price', )


# --


def batch_copy(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = ConiferProductBatchCopyAdminForm(request.POST)

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

                        if clean['needles_chk']:
                            recipient.needles = donor.needles

                        if clean['needles_chk']:
                            recipient.needles = donor.needles

                        if clean['height10_chk']:
                            recipient.height10 = donor.height10

                        if clean['width10_chk']:
                            recipient.width10 = donor.width10

                        if clean['height1_chk']:
                            recipient.height1 = donor.height1

                        if clean['width1_chk']:
                            recipient.width1 = donor.width1

                        if clean['planting_chk']:
                            recipient.planting.clear()
                            for attr in donor.planting.all():
                                recipient.planting.add(attr)

                        if clean['shelter_chk']:
                            recipient.shelter = donor.shelter

                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = ConiferProductBatchCopyAdminForm(request.POST)
    else:
        form = ConiferProductBatchCopyAdminForm(initial={
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


class ConiferProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'CON'


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
    actions = (batch_copy, make_visible, make_hidden,)
    inlines = [ConiferProductPriceInline, ImageInline, ]
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
            'fields': ('name', 'slug', 'scientific_name', 'short_description', 'needles',)
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


class ConiferProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'CON'


class ConiferProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        # qs = ConiferProductPrice.objects.exclude(container__isnull=True)\
        #     .select_related('container')\
        #     .only('container__id', 'container__name')\
        #     .order_by('container__id')\
        #     .distinct('container__id')
        # return [(o.container.id, o.container.name) for o in qs]
        qs = ConiferProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]


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
              'rs', 'shtamb', 'extra', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
