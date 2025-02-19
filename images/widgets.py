from django.utils.safestring import mark_safe
# from django.contrib.admin.widgets import AdminFileWidget
from easy_thumbnails.files import get_thumbnailer
from file_resubmit.admin import AdminResubmitImageWidget


# class ImageAdminWidget(AdminFileWidget):
class ImageAdminWidget(AdminResubmitImageWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, 'url', None):
            resize_data = self.attrs.get('resize_data', None)
            if not resize_data:
                # resize_data = {'crop': 'scale', 'size': (200, 200)}
                resize_data = {'crop': 'smart', 'size': (200, 200)}

            result = '-'
            try:
                thumbnailer = get_thumbnailer(value)
                thumb = thumbnailer.get_thumbnail(resize_data).url
                result = f'<div style="margin-right: 20px;"><a href="{value.url}" target="_blank" rel="noopener noreferrer"><img src="{thumb}" title="{value.url}"></a></div>'
                output.append(result)
            except:
                pass

        output.append(super().render(name, value, attrs))

        return mark_safe(''.join(output))
