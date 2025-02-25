from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ContactsSitemap(Sitemap):
    priority = 1

    def items(self):
        return ['contacts',]

    def location(self, obj):
        return reverse('contacts')

    # def items(self):
    #     return Contacts.objects.all().order_by('id')
    
    # def lastmod(self, obj):
    #     return obj.updated_at
