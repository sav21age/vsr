import re
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from videos.templatetags.video import get_video


class VideoAdminWidget(AdminURLFieldWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        result = ''

        if value and re.match(r'((http|https)\:\/\/)?(vk.com|vkvideo.ru)\/video-([0-9]*)_([0-9]*)', value):
            context = get_video(value, 426, 240, False)
            result = render_to_string('videos/video.html', context)
            if result:
                output.append(
                    f'<div style="margin-right: 10px;">{result}</div>'
                )

        output.append(super().render(name, value, attrs))
        return mark_safe(''.join(output))


# class VideoTextareaAdminWidget(AdminTextareaWidget):
#     def render(self, name, value, attrs=None, renderer=None):
#         output = []
#         result = ''
#         v = value
#         if v:
#             w = re.search(r'width=[\"\']([0-9]+)[\"\']', v)
#             if w is not None:
#                 v = v.replace(w.group(0), 'width="426"')

#             h = re.search(r'height=[\"\']([0-9]+)[\"\']', v)
#             if h is not None:
#                 v = v.replace(h.group(0), 'height="240"')

#             result = f'<div style="margin-right: 10px;">{v}</div>'
#             output.append(result)

#         output.append(super().render(name, value, attrs))
#         return mark_safe(''.join(output))