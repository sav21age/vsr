from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline
from images.admin import GetImageAdminMixin, ImageInline
from other.forms import OtherProductAdminForm
from other.models import OtherProduct, OtherProductCategory, OtherProductPrice


admin.site.register(OtherProductCategory)


class OtherProductPriceInline(ProductPriceInline):
    model = OtherProductPrice
    fields = ('property', 'price', )


@admin.register(OtherProduct)
class OtherProductAdmin(ProductAbstractAdmin, GetImageAdminMixin):
    list_display = ('name', 'category', 'get_image', 'is_visible')
    list_filter = ('category', )
    form = OtherProductAdminForm
    inlines = [OtherProductPriceInline, ImageInline, ]
    fieldsets = (
        ('', {
            'fields': ('is_visible',)
        }),
        ('Промо', {
            'fields': ('head_title', 'meta_description',)
        }),
        ('', {
            'fields': ('category', )
        }),
        ('', {
            'fields': ('name', 'slug', 'short_description',)
        }),
        ('', {
            'fields': ('description',)
        }),
    )


@admin.register(OtherProductPrice)
class OtherProductPriceAdmin(ProductPriceAbstractAdmin):
    fields = ('product', 'property', )
    list_display = ('product', 'property', 'price',)
