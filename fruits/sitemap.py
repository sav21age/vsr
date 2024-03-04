from django.contrib.sitemaps import Sitemap
from fruits.models import FruitProduct


class FruitProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return FruitProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
