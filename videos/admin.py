from django.contrib.contenttypes.admin import GenericStackedInline
# from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableGenericInlineAdminMixin
from common.widgets import formfield_overrides
from videos.forms import VideoAdminForm
from videos.models import Video


class VideoInline(SortableGenericInlineAdminMixin, GenericStackedInline):
    model = Video
    form = VideoAdminForm
    extra = 0
    show_change_link = True
    formfield_overrides = formfield_overrides
    # verbose_name = "Видео из ВК"
    verbose_name_plural = "Видео из ВК"
    max_num = 5
    # classes = ['collapse',]
