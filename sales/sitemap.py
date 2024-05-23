from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class SaleSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['sale',]

    def location(self, obj):
        return reverse('sale_list')
