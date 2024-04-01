from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class CatalogSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['catalog',]

    def location(self, obj):
        return reverse('catalog_item_list')
