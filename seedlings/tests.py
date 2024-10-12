from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse


APP = 'seedlings'


class RoseProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse(f"{APP}:list"))
        self.assertEqual(response.status_code, 200)

    def test_listview_per_page(self):
        """ Test ListView with per_page """
        per_page = [8, 12, 24, 36, 'test', None, '']

        for value in per_page:
            kwargs = {'per_page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

    def test_listview_pagination(self):
        """ Test ListView with pagination """

        page = (1,)
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        page = (100000000, 'test')
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)
