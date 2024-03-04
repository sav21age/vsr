from django.contrib.sitemaps import Sitemap
from deciduous.models import DecProduct


class DecProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return DecProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
