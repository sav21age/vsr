
from django.template import Context, Template
from django.test import TestCase


class VideoTemplateTagTest(TestCase):

    def test_get_video(self):
        r = '\n<iframe src="https://vk.com/video_ext.php?oid=-129700322&id=456239108&hd=2&autoplay=0&js_api=1" width="853" height="480" allow="autoplay; encrypted-media; fullscreen; picture-in-picture; screen-wake-lock;" frameborder="0" allowfullscreen></iframe>\n'
        t = Template(
            "{% load video %}"
            "{% get_video 'https://vk.com/video-129700322_456239108' %}"
        ).render(Context({}))
        self.assertEqual(t, r)

        r = '\n<iframe src="https://vk.com/video_ext.php?oid=-129700322&id=456239108&hd=2&autoplay=0" width="426" height="240" allow="autoplay; encrypted-media; fullscreen; picture-in-picture; screen-wake-lock;" frameborder="0" allowfullscreen></iframe>\n'
        t = Template(
            "{% load video %}"
            "{% get_video 'https://vk.com/video-129700322_456239108' 426 240 False %}"
        ).render(Context({}))
        self.assertEqual(t, r)

        t = Template(
            "{% load video %}"
            "{% get_video 'https://vk.com/video_129700322_456239108' %}"
        ).render(Context({}))
        self.assertEqual(t, '')

        t = Template(
            "{% load video %}"
            "{% get_video 'https://vk.com/video_129700322' %}"
        ).render(Context({}))
        self.assertEqual(t, '')
