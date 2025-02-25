from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PriceListSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['price_list',]

    def location(self, obj):
        return reverse('price_list_detail')
