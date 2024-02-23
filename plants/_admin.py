from common.helpers import formfield_overrides
from images.admin import ImageInline
from images.models import Image
from django.contrib.contenttypes import fields
from django.db import models
from django.contrib import admin
from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin
from plants.forms import ProductAdminForm
from django.contrib.admin import SimpleListFilter

from plants.models import (
    PlantAdvantage, PlantPriceContainer, PlantDivision, PlantGenius, PlantGroup,
    PlantPrice, PlantProduct, PlantPriceRootSystem, PlantPriceTrunkDiameter, 
    PlantPriceHeight,  PlantPriceWidth, )


class PlantPriceInline(SortableInlineAdminMixin, admin.StackedInline):
    model = PlantPrice
    # form = ImageAdminForm
    extra = 0
    show_change_link = True
    # formfield_overrides = formfield_overrides
    # verbose_name = "Картинка"
    # verbose_name_plural = "Картинки"


# class PageAdmin(admin.ModelAdmin):
#     save_on_top = True
#     form = PageAdminForm
#     prepopulated_fields = {'slug': ('h1', )}
#     formfield_overrides = formfield_overrides
#     fieldsets = (
#         ('', {
#             'fields': ('is_visible',)
#         }),
#         ('Заголовок и мета теги страницы', {
#             'fields': ('head_title', 'meta_description',)
#         }),
#         ('Имя и url-адрес страницы', {
#             'fields': ('h1', 'slug',)
#         }),
#     )

class PlantDivisionFilter(SimpleListFilter):
    title = 'Отдел'
    parameter_name = 'division'

    def lookups(self, request, model_admin):
        qs = PlantDivision.objects.all()
        return [(o.id, o.name) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group__genius__division=self.value())
        return queryset


class PlantGeniusFilter(SimpleListFilter):
    title = 'Род'
    parameter_name = 'genius'

    def lookups(self, request, model_admin):
        qs = PlantGenius.objects.all()
        return [(o.id, o.name) for o in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group__genius=self.value())
        return queryset
        

class PlantProductAdmin(SortableAdminBase, admin.ModelAdmin):
    save_on_top = True
    form = ProductAdminForm
    inlines = [PlantPriceInline, ImageInline, ]
    prepopulated_fields = {'slug': ('name', )}
    filter_horizontal = ('advantages', )
    formfield_overrides = formfield_overrides
    list_filter = (PlantDivisionFilter, PlantGeniusFilter, )
    # list_filter = ('group', )
    search_fields = ('name',)
    search_help_text = 'Поиск по названию'
    # autocomplete_fields = ["name",]
    fieldsets = (
        ('', {
            'fields': ('is_visible',)
        }),
        ('Промо', {
            'fields': ('head_title', 'meta_description',)
        }),
        ('Классификация растений', {
            'fields': ('division', 'genius', 'group', )
        }),        
        ('Товар', {
            'fields': ('name', 'slug', 'size', 'advantages', 'features', 'description', )
        }),
    )


@admin.register(PlantPriceHeight)
class PlantPriceHeightAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False


@admin.register(PlantPriceWidth)
class PlantPriceWidthAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False


admin.site.register(PlantProduct, PlantProductAdmin)
admin.site.register(PlantDivision)
admin.site.register(PlantGenius)
admin.site.register(PlantGroup)
# admin.site.register(PlantHeight)
admin.site.register(PlantAdvantage)
admin.site.register(PlantPriceTrunkDiameter)
# admin.site.register(PlantWidth)
admin.site.register(PlantPriceRootSystem)

admin.site.register(PlantPriceContainer)
