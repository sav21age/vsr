from django.contrib import admin
from common.admin import ProductAbstractAdmin, ProductPriceAbstractAdmin, ProductPriceInline, make_hidden, make_visible
from images.admin import GetImageAdminMixin, ImageInline
from other.forms import OtherProductAdminForm
from other.models import OtherProduct, OtherProductCategory, OtherProductPrice
from videos.admin import VideoInline


admin.site.register(OtherProductCategory)


class OtherProductPriceInline(ProductPriceInline):
    model = OtherProductPrice
    fields = ('name', 'price', 'updated_at', )


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
    inlines = [ImageInline, VideoInline, OtherProductPriceInline,]
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
            'fields': ('name', 'name_trans_words', 'slug', 'short_description',)
        }),
        ('', {
            'fields': ('description',)
        }),
    )


@admin.register(OtherProductPrice)
class OtherProductPriceAdmin(ProductPriceAbstractAdmin):
    fields = ('product', 'name', 'price',)
    list_display = ('product', 'name', 'updated_at', 'price',)
