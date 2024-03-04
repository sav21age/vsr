from django.contrib import admin
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from catalog.forms import CatalogItemAdminForm
from catalog.models import CatalogItem
from common.helpers import formfield_overrides


@admin.register(CatalogItem)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image', 'order_number',)
    list_editable = ('order_number',)
    form = CatalogItemAdminForm
    formfield_overrides = formfield_overrides
    
    @mark_safe
    def get_image(self, obj):
        try:
            if obj.image_path:
                thumb = get_thumbnailer(obj.image_path)['detail_thumbnail'].url
                return '<a href="{i}" target="_blank" rel="noopener noreferrer"><img src="{t}" title="{i}"></a>'.format(
                    i=obj.image_path.url,
                    t=thumb
                )
        except:
            return ''
    get_image.short_description = 'Картинка'
