from django.contrib.sitemaps import Sitemap
from roses.models import RoseProduct


class RoseProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return RoseProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
