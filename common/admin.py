import re

from adminsortable2.admin import SortableAdminBase
from django.contrib import admin

from common.widgets import formfield_overrides
from images.admin import GetImageAdminMixin


def make_visible(modeladmin, request, queryset):
    queryset.update(is_visible=True)
make_visible.short_description = 'Показывать'


def make_hidden(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_visible = False
        obj.save()
make_hidden.short_description = 'Скрыть'


# class ProductPriceInline(SortableInlineAdminMixin, admin.StackedInline):
class ProductPriceInline(admin.StackedInline):
    extra = 0
    show_change_link = True
    readonly_fields = ('updated_at', )


class PageAbstractAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    save_on_top = True
    prepopulated_fields = {'slug': ('name', )}
    list_per_page = 40
    formfield_overrides = formfield_overrides
    fieldsets = (
        ('', {
            'fields': ('is_visible',)
        }),
        ('Промо', {
            'fields': ('head_title', 'meta_description',)
        }),
        ('', {
            'fields': ('name', 'slug',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.head_title = obj.head_title.strip()
        obj.head_title = re.sub(r'\s+', ' ', obj.head_title)
        super().save_model(request, obj, form, change)


class GetMinPriceAdminMixin():
    def get_min_price(self, obj):
        try:
            if obj.get_min_price is not None:
                return f"{obj.get_min_price} руб."
            return 'нет в наличии'
        except:
            return '-'
    get_min_price.short_description = 'Минимальная цена'


class ProductAbstractAdmin(SortableAdminBase, PageAbstractAdmin, GetImageAdminMixin, GetMinPriceAdminMixin):
    search_fields = ('name', 'name_trans_words',)
    search_help_text = 'Поиск по названию и переводу слов'
    list_display = ('name', 'get_image', 'is_visible', 'get_min_price',)

    def save_model(self, request, obj, form, change):
        obj.name = obj.name.strip()
        obj.name = re.sub(r'\s+', ' ', obj.name)
        super().save_model(request, obj, form, change)


class ProductPriceAbstractAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    search_fields = ('product__name',)
    search_help_text = 'Поиск по названию'
    readonly_fields = ('updated_at',)
    list_editable = ('price', )
    ordering = ('product__name', 'price', )
    list_per_page = 30

    # def has_add_permission(self, request, obj=None):
    #     return False    