from django.test import Client, TestCase
from django.urls import reverse


class SaleTest(TestCase):
    fixtures = ['fixtures/sales.json', ]

    def setUp(self):
        self.client = Client()

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse('sale_list'))
        self.assertEqual(response.status_code, 200)