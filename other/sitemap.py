from django.contrib.sitemaps import Sitemap
from other.models import OtherProduct


class OtherProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return OtherProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
