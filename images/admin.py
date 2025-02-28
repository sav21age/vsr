from django.contrib.contenttypes.admin import GenericStackedInline
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from images.forms import ImageAdminForm
from images.models import Image
from common.widgets import formfield_overrides
from adminsortable2.admin import SortableGenericInlineAdminMixin
# from file_resubmit.admin import AdminResubmitMixin


# class ImageInline(SortableGenericInlineAdminMixin, AdminResubmitMixin, GenericStackedInline):
class ImageInline(SortableGenericInlineAdminMixin, GenericStackedInline):
    model = Image
    form = ImageAdminForm
    extra = 0
    show_change_link = True
    formfield_overrides = formfield_overrides
    # verbose_name = "Картинка"
    # verbose_name_plural = "Картинки"


class GetImageAdminMixin():
    @mark_safe
    def get_image(self, obj):
        try:
            if obj.images.all():
                thumb = get_thumbnailer(obj.get_image.path)[
                    'detail_thumbnail'].url
                return '<a href="{i}" target="_blank" rel="noopener noreferrer"><img src="{t}" title="{i}"></a>'.format(
                    i=obj.get_image.path.url,
                    t=thumb
                )
        except:
            return ''
    get_image.short_description = 'Картинка'
