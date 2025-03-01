from django.test import TestCase, Client
from django.urls import reverse


class SitemapTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_sitemap(self):
        """ Test sitemap """
        response = self.client.get(
            reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
        