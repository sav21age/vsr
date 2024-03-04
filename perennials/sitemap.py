from django.contrib.sitemaps import Sitemap
from perennials.models import PerProduct


class PerProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return PerProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
