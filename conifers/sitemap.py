from django.contrib.sitemaps import Sitemap
from conifers.models import ConiferProduct


class ConiferProductSitemap(Sitemap):
    priority = 1

    def items(self):
        return ConiferProduct.is_visible_objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at
