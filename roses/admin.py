from django.contrib import admin
from django.shortcuts import render
from django.db import transaction
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages
from django.http import HttpResponseRedirect
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from common.filters import ProductPriceContainerAdminFilter
from common.helpers import get_price_properties
from images.admin import ImageInline
from plants.models import PlantPriceContainer
from roses.forms import RoseProductAdminForm, RoseProductBatchCopyAdminForm, RoseSpeciesAdminForm
from roses.models import RoseProduct, RoseProductPrice, RoseSpecies

@admin.register(RoseSpecies)
class RoseSpeciesAdmin(admin.ModelAdmin):
    form = RoseSpeciesAdminForm


class RoseProductPriceInline(ProductPriceInline):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .select_related('container')

    model = RoseProductPrice
    fields = ('container', 'price', )


# --
    

def batch_copy(modeladmin, request, queryset):
    if 'do_action' in request.POST:
        form = RoseProductBatchCopyAdminForm(request.POST)

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

                        if clean['flowering_chk']:
                            recipient.flowering = donor.flowering

                        if clean['quantity_on_stem_chk']:
                            recipient.quantity_on_stem = donor.quantity_on_stem

                        if clean['flavor_chk']:
                            recipient.flavor = donor.flavor
                        
                        if clean['flower_size_chk']:
                            recipient.flower_size = donor.flower_size
                        
                        if clean['resistance_fungus_chk']:
                            recipient.resistance_fungus = donor.resistance_fungus

                        if clean['resistance_rain_chk']:
                            recipient.resistance_rain = donor.resistance_rain
                        
                        if clean['shelter_winter_chk']:
                            recipient.shelter_winter = donor.shelter_winter
                        
                        if clean['winter_zone_chk']:
                            recipient.winter_zone = donor.winter_zone
                        
                        if clean['advantages_chk']:
                            recipient.advantages.clear()
                            for attr in donor.advantages.all():
                                recipient.advantages.add(attr)
                        recipient.save()
                except:
                    messages.error(request, 'Произошла ошибка')
            messages.success(request, 'Своиства успешно скопированы')
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = RoseProductBatchCopyAdminForm(request.POST)
    else:
        form = RoseProductBatchCopyAdminForm(initial={
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


@admin.register(RoseProduct)
class RoseProductAdmin(ProductAbstractAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('roseproductprice_set')

    form = RoseProductAdminForm
    show_facets = admin.ShowFacets.ALWAYS
    list_filter = ('species', )
    actions = (batch_copy, )
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
