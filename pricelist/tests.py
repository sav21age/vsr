from django.test import TestCase, Client
from django.urls import reverse


class PriceListTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test ListView """
        response = self.client.get(reverse('price_list_detail'))
        self.assertEqual(response.status_code, 200)