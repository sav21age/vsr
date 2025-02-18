from django.contrib import admin
# from django.contrib.contenttypes.models import ContentType
from adminsortable2.admin import SortableAdminBase
# from carts.models import CartItem
from common.helpers import formfield_overrides
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


class GetMinPriceAdminMixin():
    def get_min_price(self, obj):
        try:
            if obj.get_min_price:
                return f"{obj.get_min_price} руб."
            return 'нет в наличии'
        except:
            return '-'
    get_min_price.short_description = 'Минимальная цена'


class ProductAbstractAdmin(SortableAdminBase, PageAbstractAdmin, GetImageAdminMixin, GetMinPriceAdminMixin):
    search_fields = ('name', 'name_trans_words',)
    search_help_text = 'Поиск по названию и переводу слов'
    list_display = ('name', 'get_image', 'is_visible', 'get_min_price',)


class ProductPriceAbstractAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    search_fields = ('product__name',)
    search_help_text = 'Поиск по названию'
    readonly_fields = ('product', 'updated_at',)
    list_editable = ('price', )
    ordering = ('product__name', 'price', )
    list_per_page = 30

    def has_add_permission(self, request, obj=None):
        return False    