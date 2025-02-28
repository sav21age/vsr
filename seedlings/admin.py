from django.contrib import admin
from seedlings.forms import SeedlingAdminForm
from seedlings.models import Seedling
from common.widgets import formfield_overrides
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


@admin.register(Seedling)
class SeedlingAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image', 'is_visible',)
    list_filter = ('division',)
    formfield_overrides = formfield_overrides
    form = SeedlingAdminForm

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
