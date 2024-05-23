from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class SalesSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['sales',]

    def location(self, obj):
        return reverse('sales')
