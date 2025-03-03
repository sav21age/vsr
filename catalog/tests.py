from django.test import Client, TestCase
from django.urls import reverse


class CatalogTest(TestCase):
    fixtures = ['fixtures/catalog.json', ]

    def setUp(self):
        self.client = Client()

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse('catalog_item_list'))
        self.assertEqual(response.status_code, 200)