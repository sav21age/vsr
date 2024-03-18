from django.test import TestCase, Client
from django.urls import reverse


class IndexTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_index(self):
        """ Test index """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
