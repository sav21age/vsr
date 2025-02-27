from django.test import TestCase, Client
from django.urls import reverse


class PriceDetailTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """
        response = self.client.get(reverse('price_list_detail'))
        self.assertEqual(response.status_code, 200)


class PriceDetailTestNotExists(TestCase):
    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """
        response = self.client.get(reverse('price_list_detail'))
        self.assertEqual(response.status_code, 404)
