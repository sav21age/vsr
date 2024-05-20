from django.contrib import admin
from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from common.filters import (
    ProductGenusAdminFilter, ProductPriceContainerAdminFilter, ProductPriceGenusAdminFilter, SpeciesGenusAdminFilter)
from deciduous.forms import DecProductAdminForm, DecProductBatchCopyAdminForm, DecSpeciesAdminForm
from deciduous.models import DecProduct, DecProductPrice, DecSpecies
from images.admin import ImageInline
from plants.admin import PlantSpeciesAbstractAdmin
from plants.models import PlantPriceContainer


class DecSpeciesGenusAdminFilter(SpeciesGenusAdminFilter):
    division_name = 'DEC'


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
              'rs', 'shtamb', 'extra', 'bush', 'price', )


# --


def batch_copy(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = DecProductBatchCopyAdminForm(request.POST)

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

                        if clean['leaves_chk']:
                            recipient.leaves = donor.leaves

                        if clean['crown_chk']:
                            recipient.crown = donor.crown

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['flowering_period_chk']:
                            recipient.flowering_period = donor.flowering_period

                        if clean['flower_size_chk']:
                            recipient.flower_size = donor.flower_size

                        if clean['inflorescence_chk']:
                            recipient.inflorescence = donor.inflorescence

                        if clean['inflorescence_size_chk']:
                            recipient.inflorescence_size = donor.inflorescence_size

                        if clean['planting_chk']:
                            recipient.planting.clear()
                            for attr in donor.planting.all():
                                recipient.planting.add(attr)

                        if clean['shelter_winter_chk']:
                            recipient.shelter_winter = donor.shelter_winter

                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone

                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = DecProductBatchCopyAdminForm(request.POST)
    else:
        form = DecProductBatchCopyAdminForm(initial={
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


class DecProductGenusAdminFilter(ProductGenusAdminFilter):
    division_name = 'DEC'


@admin.register(DecProduct)
class DecProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    form = DecProductAdminForm
    list_filter = (DecProductGenusAdminFilter, )
    actions = (batch_copy, make_visible, make_hidden,)
    inlines = [ImageInline,  DecProductPriceInline, ]
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


class DecProductPriceGenusAdminFilter(ProductPriceGenusAdminFilter):
    division_name = 'DEC'


class DecProductPriceContainerAdminFilter(ProductPriceContainerAdminFilter):
    def lookups(self, request, model_admin):
        qs = DecProductPrice.objects.exclude(container_id__isnull=True)\
            .order_by('container_id')\
            .distinct('container_id')\
            .values_list('container_id', flat=True)

        lst = list(qs)

        qs = PlantPriceContainer.objects.filter(id__in=lst)\
            .order_by('order_number')

        return [(o.id, o.name) for o in qs]


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
              'rs', 'shtamb', 'extra', 'bush', 'price', )
    list_display = ('get_product', 'price', )

    def get_product(self, obj=None):
        if obj:
            # return f"{obj.product} {get_price_properties(obj)}"
            return f"{obj.product} {obj.get_complex_name}"
        return ''
    get_product.short_description = 'растение'
