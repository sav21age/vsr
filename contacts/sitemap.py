from django.contrib.sitemaps import Sitemap
from contacts.models import Contacts


class ContactsSitemap(Sitemap):
    priority = 0.5
    
    def items(self):
        # return ['contacts']
        return Contacts.objects.all().order_by('id')
    
    def lastmod(self, obj):
        return obj.updated_at

    # def location(self, item):
        # return reverse(item)

    # def location(self, obj):
    #     return reverse('contacts')
