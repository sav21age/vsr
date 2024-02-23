from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from easy_thumbnails.files import get_thumbnailer


class ImageAdminWidget(AdminFileWidget):
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
                result = '<div style="margin-right: 20px;"><a href="{i}" target="_blank" rel="noopener noreferrer"><img src="{t}" title="{i}"></a></div>'.format(
                         i=value.url,
                         t=thumb
                )
                output.append(result)
            except Exception as e:
                # logger.error(e)
                pass

        output.append(super().render(name, value, attrs))

        return mark_safe(''.join(output))
