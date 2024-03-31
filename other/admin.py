from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from images.admin import GetImageAdminMixin, ImageInline
from other.forms import OtherProductAdminForm
from other.models import OtherProduct, OtherProductCategory, OtherProductPrice


admin.site.register(OtherProductCategory)


class OtherProductPriceInline(ProductPriceInline):
    model = OtherProductPrice
    fields = ('name', 'price', )


@admin.register(OtherProduct)
class OtherProductAdmin(ProductAbstractAdmin, GetImageAdminMixin):
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('images') \
            .prefetch_related('prices')

    list_display = ('name', 'category', 'get_image', 'is_visible')
    list_filter = ('category', )
    form = OtherProductAdminForm
    actions = (make_visible, make_hidden,)
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
    fields = ('product', 'name', )
    list_display = ('product', 'name', 'price',)
