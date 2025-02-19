from django import template


register = template.Library()


@register.inclusion_tag("videos/video.html")
def get_video(url, width=853, height=480, js_api=True):
    # url = 'https://vk.com/video-129700322_456239108'

    # - 426 x 240
    # hd
    # 1 - 640 x 360
    # 2 - 853 x 480
    # 3 - 1280 x 720
    # 4 - 1920 x 1080
    
    try:
        pos = url.index('-')
        url = url[pos:].split('_', 1)
    except:
        return {'show': False, }
    
    if len(url) != 2:
        return {'show': False,}
    
    return {
        'show': True,
        'oid': url[0],
        'id': url[1],
        'width': width,
        'height': height,
        'js_api': js_api,
    }
