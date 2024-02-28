from django.contrib import admin
from adminsortable2.admin import SortableAdminBase
from common.helpers import formfield_overrides


# class ProductPriceInline(SortableInlineAdminMixin, admin.StackedInline):
class ProductPriceInline(admin.StackedInline):
    extra = 0
    show_change_link = True


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


class ProductAbstractAdmin(SortableAdminBase, PageAbstractAdmin):
    search_fields = ('name',)
    search_help_text = 'Поиск по названию'


class ProductPriceAbstractAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    search_fields = ('product__name',)
    search_help_text = 'Поиск по названию'
    readonly_fields = ('product', )
    list_editable = ('price', )
    ordering = ('product__name', 'price', )
    list_per_page = 30

    def has_add_permission(self, request, obj=None):
        return False
