from django import forms
from videos.models import Video
from videos.widgets import VideoAdminWidget


class VideoAdminForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['code'].widget = textarea_widget

    class Meta:
        model = Video
        widgets = {
            # 'code': VideoTextareaAdminWidget(attrs={'rows': 4, 'style': 'width: 100%; font-size: 115%;'}),
            'url': VideoAdminWidget(attrs={'style': 'font-size: 120%; height: 18px;'}),
        }
        exclude = []

    # def clean_url(self):
    #     url = self.cleaned_data['url']

    #     if not re.match(r'((http|https)\:\/\/)?(vk.com|vkvideo.ru)\/video-([0-9]*)_([0-9]*)', url):
    #         raise forms.ValidationError('Не правильная ссылка.')

    #     return url
